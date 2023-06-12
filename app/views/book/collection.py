from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required

from app.controllers import (
    create_breadcrumbs,
    register_book_verify_route,
)
from app.controllers.delete_nested_book_entities import (
    delete_nested_collection_entities,
)
from app import models as m, db, forms as f
from app.controllers.require_permission import require_permission
from app.logger import log
from .bp import bp


@bp.route("/<int:book_id>/collections", methods=["GET"])
def collection_view(book_id: int):
    book = db.session.get(m.Book, book_id)
    breadcrumbs = create_breadcrumbs(book_id=book_id)
    if not book or book.is_deleted:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.my_library"))
    else:
        return render_template(
            "book/collection_view.html", book=book, breadcrumbs=breadcrumbs
        )


@bp.route("/<int:book_id>/create_collection", methods=["POST"])
@bp.route("/<int:book_id>/<int:collection_id>/create_sub_collection", methods=["POST"])
@register_book_verify_route(bp.name)
@require_permission(
    entity_type=m.Permission.Entity.COLLECTION,
    access=[m.Permission.Access.C],
    entities=[m.Collection, m.Book],
)
@login_required
def collection_create(book_id: int, collection_id: int | None = None):
    book: m.Book = db.session.get(m.Book, book_id)

    parent_collection: m.Collection = None
    redirect_url = url_for("book.collection_view", book_id=book_id)
    if collection_id:
        parent_collection: m.Collection = db.session.get(m.Collection, collection_id)
        if parent_collection.is_leaf:
            log(log.WARNING, "Collection with id [%s] is leaf", collection_id)
            flash("You can't create subcollection for this collection", "danger")
            return redirect(
                url_for(
                    "book.collection_view",
                    book_id=book_id,
                    collection_id=collection_id,
                )
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

        position = 0
        if parent_collection and parent_collection.active_children:
            position = len(parent_collection.active_children)

        collection: m.Collection = m.Collection(
            label=label,
            about=form.about.data,
            parent_id=book.versions[-1].root_collection.id,
            version_id=book.active_version.id,
            position=position,
        )
        if collection_id:
            collection.parent_id = collection_id

        log(log.INFO, "Create collection [%s]. Book: [%s]", collection, book.id)
        collection.save()

        for access_group in collection.parent.access_groups:
            m.CollectionAccessGroups(
                collection_id=collection.id, access_group_id=access_group.id
            ).save()

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
@register_book_verify_route(bp.name)
@require_permission(
    entity_type=m.Permission.Entity.COLLECTION,
    access=[m.Permission.Access.U],
    entities=[m.Collection],
)
@login_required
def collection_edit(book_id: int, collection_id: int):
    book: m.Book = db.session.get(m.Book, book_id)
    collection: m.Collection = db.session.get(m.Collection, collection_id)

    form = f.EditCollectionForm()
    redirect_url = url_for(
        "book.collection_view",
        book_id=book_id,
    )

    if form.validate_on_submit():
        label = form.label.data
        existing_collection: m.Collection = (
            m.Collection.query.filter_by(
                is_deleted=False, label=label, parent_id=collection.parent.id
            )
            .filter(m.Collection.id != collection.id)
            .first()
        )

        if existing_collection:
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
@register_book_verify_route(bp.name)
@require_permission(
    entity_type=m.Permission.Entity.COLLECTION,
    access=[m.Permission.Access.D],
    entities=[m.Collection],
)
@login_required
def collection_delete(book_id: int, collection_id: int):
    collection: m.Collection = db.session.get(m.Collection, collection_id)

    collection.is_deleted = True
    if collection.active_children:
        for child in collection.active_children:
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


# TODO permission check
# @require_permission(
#     entity_type=m.Permission.Entity.COLLECTION,
#     access=[m.Permission.Access.C],
#     entities=[m.Collection, m.Book],
# )
@bp.route(
    "/<int:book_id>/<int:collection_id>/collection/change_position", methods=["POST"]
)
@register_book_verify_route(bp.name)
@login_required
def change_collection_position(book_id: int, collection_id: int):
    collection: m.Collection = db.session.get(m.Collection, collection_id)
    new_position = request.json.get("position")
    collection_id = request.json.get("collection_id")

    new_parent: m.Collection = collection.parent
    if collection_id is not None:
        new_parent: m.Collection = db.session.get(m.Collection, collection_id)
        if not new_parent:
            log(log.INFO, "Collection with id [%s] not found", collection_id)
            return {"message": "new parent collection not found"}, 404

        log(
            log.INFO,
            "Change collection [%s] parent_id to [%s]",
            collection,
            collection_id,
        )
        collection.parent_id = collection_id

    if new_parent.active_children:
        collections_to_edit = (
            m.Collection.query.filter(
                m.Collection.parent_id == new_parent.id,
                m.Collection.id != collection.id,
            )
            .order_by(m.Collection.position)
            .all()
        )
        collections_to_edit.insert(new_position, collection)
        log(
            log.INFO,
            "Calculate new positions of collections in [%s]",
            new_parent,
        )
        for position in range(len(collections_to_edit)):
            collections_to_edit[position].position = position
            collections_to_edit[position].save(False)
    else:
        log(
            log.INFO,
            "Collection [%s] does not have active collection. Set collection [%s] position to 1",
            collection,
            new_parent,
        )
        collection.position = 1

    log(log.INFO, "Apply position changes on [%s]", collection)
    db.session.commit()
    return {"message": "success"}
