from flask import (
    render_template,
    flash,
    redirect,
    url_for,
)
from flask_login import login_required

from app.controllers import (
    create_breadcrumbs,
    register_book_verify_route,
)
from app.controllers.delete_nested_book_entities import (
    delete_nested_collection_entities,
)
from app import models as m, db, forms as f
from app.logger import log
from .bp import bp


@bp.route("/<int:book_id>/collections", methods=["GET"])
def collection_view(book_id: int):
    book = db.session.get(m.Book, book_id)
    breadcrumbs = create_breadcrumbs(book_id=book_id, collection_path=())
    if not book or book.is_deleted:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.my_library"))
    else:
        return render_template(
            "book/collection_view.html", book=book, breadcrumbs=breadcrumbs
        )


@bp.route("/<int:book_id>/<int:collection_id>/subcollections", methods=["GET"])
def sub_collection_view(book_id: int, collection_id: int):
    book: m.Book = db.session.get(m.Book, book_id)
    if not book or book.is_deleted:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.my_library"))
    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if not collection or collection.is_deleted:
        log(log.WARNING, "Collection with id [%s] not found", collection_id)
        flash("Collection not found", "danger")
        return redirect(url_for("book.collection_view", book_id=book_id))
    breadcrumbs = create_breadcrumbs(book_id=book_id, collection_path=(collection.id,))
    if collection.is_leaf:
        return redirect(
            url_for("book.section_view", book_id=book.id, collection_id=collection.id)
        )
    else:
        return render_template(
            "book/sub_collection_view.html",
            book=book,
            collection=collection,
            breadcrumbs=breadcrumbs,
        )


@bp.route("/<int:book_id>/create_collection", methods=["POST"])
@bp.route("/<int:book_id>/<int:collection_id>/create_sub_collection", methods=["POST"])
@register_book_verify_route(bp.name)
@login_required
def collection_create(book_id: int, collection_id: int | None = None):
    book: m.Book = db.session.get(m.Book, book_id)

    redirect_url = url_for("book.collection_view", book_id=book_id)
    if collection_id:
        collection: m.Collection = db.session.get(m.Collection, collection_id)
        if collection.is_leaf:
            log(log.WARNING, "Collection with id [%s] is leaf", collection_id)
            flash("You can't create subcollection for this collection", "danger")
            return redirect(
                url_for(
                    "book.sub_collection_view",
                    book_id=book_id,
                    collection_id=collection_id,
                )
            )

        redirect_url = url_for(
            "book.sub_collection_view", book_id=book_id, collection_id=collection_id
        )

    form = f.CreateCollectionForm()

    if form.validate_on_submit():
        label = form.label.data
        collection: m.Collection = m.Collection.query.filter_by(
            is_deleted=False,
            label=label,
        )
        if collection_id:
            collection = collection.filter_by(parent_id=collection_id)
        else:
            collection = collection.filter_by(
                parent_id=book.versions[-1].root_collection.id
            )
        collection = collection.first()

        if collection:
            log(
                log.INFO,
                "Collection with similar label already exists. Book: [%s], Collection: [%s], Label: [%s]",
                book.id,
                collection.id,
                label,
            )
            flash("Collection label must be unique!", "danger")
            return redirect(redirect_url)

        collection: m.Collection = m.Collection(
            label=label,
            about=form.about.data,
            parent_id=book.versions[-1].root_collection.id,
        )
        if collection_id:
            collection.parent_id = collection_id
            collection.is_leaf = True

        log(log.INFO, "Create collection [%s]. Book: [%s]", collection, book.id)
        collection.save()

        flash("Success!", "success")
        if collection_id:
            redirect_url = url_for("book.collection_view", book_id=book_id)
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Collection/Subcollection create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(redirect_url)


@bp.route("/<int:book_id>/<int:collection_id>/edit", methods=["POST"])
@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/edit", methods=["POST"]
)
@register_book_verify_route(bp.name)
@login_required
def collection_edit(
    book_id: int, collection_id: int, sub_collection_id: int | None = None
):
    book: m.Book = db.session.get(m.Book, book_id)
    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if sub_collection_id:
        collection = db.session.get(m.Collection, sub_collection_id)

    form = f.EditCollectionForm()
    redirect_url = url_for(
        "book.collection_view",
        book_id=book_id,
    )

    if form.validate_on_submit():
        label = form.label.data
        collection_query: m.Collection = m.Collection.query.filter_by(
            is_deleted=False,
            label=label,
        ).filter(m.Collection.id != collection.id)

        if sub_collection_id:
            collection_query = collection_query.filter_by(parent_id=collection_id)
        else:
            collection_query = collection_query.filter_by(
                parent_id=collection.parent.id
            )

        if collection_query.first():
            log(
                log.INFO,
                "Collection with similar label already exists. Book: [%s], Collection: [%s], Label: [%s]",
                book.id,
                collection_id,
                label,
            )
            flash("Collection label must be unique!", "danger")
            return redirect(redirect_url)

        if label:
            collection.label = label

        about = form.about.data
        if about:
            collection.about = about

        log(log.INFO, "Edit collection [%s]", collection.id)
        collection.save()

        flash("Success!", "success")
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Collection edit errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(redirect_url)


@bp.route("/<int:book_id>/<int:collection_id>/delete", methods=["POST"])
@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/delete",
    methods=["POST"],
)
@register_book_verify_route(bp.name)
@login_required
def collection_delete(
    book_id: int, collection_id: int, sub_collection_id: int | None = None
):
    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if sub_collection_id:
        collection: m.Collection = db.session.get(m.Collection, sub_collection_id)

    collection.is_deleted = True
    if collection.children:
        for child in collection.children:
            child: m.Collection
            delete_nested_collection_entities(child)
            log(log.INFO, "Delete subcollection [%s]", collection.id)
            child.save()
    delete_nested_collection_entities(collection)
    collection.save()

    flash("Success!", "success")
    return redirect(
        url_for(
            "book.collection_view",
            book_id=book_id,
        )
    )
