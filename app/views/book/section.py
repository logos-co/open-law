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
    delete_nested_section_entities,
)
from app import models as m, db, forms as f
from app.logger import log
from .bp import bp


@bp.route("/<int:book_id>/<int:collection_id>/sections", methods=["GET"])
@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/sections",
    methods=["GET"],
)
def section_view(
    book_id: int, collection_id: int, sub_collection_id: int | None = None
):
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

    sub_collection = None
    if sub_collection_id:
        sub_collection: m.Collection = db.session.get(m.Collection, sub_collection_id)
        if not sub_collection or sub_collection.is_deleted:
            log(log.WARNING, "Sub_collection with id [%s] not found", sub_collection_id)
            flash("Sub_collection not found", "danger")
            return redirect(
                url_for(
                    "book.sub_collection_view",
                    book_id=book_id,
                    collection_id=collection_id,
                )
            )

    if sub_collection:
        sections = sub_collection.active_sections
    else:
        sections = collection.active_sections

    breadcrumbs = create_breadcrumbs(
        book_id=book_id,
        collection_path=(
            collection_id,
            sub_collection_id,
        ),
    )

    return render_template(
        "book/section_view.html",
        book=book,
        collection=collection,
        sections=sections,
        sub_collection=sub_collection,
        breadcrumbs=breadcrumbs,
    )


@bp.route("/<int:book_id>/<int:collection_id>/create_section", methods=["POST"])
@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/create_section",
    methods=["POST"],
)
@register_book_verify_route(bp.name)
@login_required
def section_create(
    book_id: int, collection_id: int, sub_collection_id: int | None = None
):
    book: m.Book = db.session.get(m.Book, book_id)
    collection: m.Collection = db.session.get(m.Collection, collection_id)
    sub_collection = None
    if sub_collection_id:
        sub_collection: m.Collection = db.session.get(m.Collection, sub_collection_id)

    redirect_url = url_for("book.collection_view", book_id=book_id)
    if collection_id:
        redirect_url = url_for(
            "book.section_view",
            book_id=book_id,
            collection_id=collection_id,
            sub_collection_id=sub_collection_id,
        )

    form = f.CreateSectionForm()

    if form.validate_on_submit():
        section: m.Section = m.Section(
            label=form.label.data,
            about=form.about.data,
            collection_id=sub_collection_id or collection_id,
            version_id=book.last_version.id,
        )
        if sub_collection:
            sub_collection.is_leaf = True
        else:
            collection.is_leaf = True
        log(log.INFO, "Create section [%s]. Collection: [%s]", section, collection_id)
        section.save()

        flash("Success!", "success")
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Section create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(redirect_url)


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:section_id>/edit_section", methods=["POST"]
)
@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/<int:section_id>/edit_section",
    methods=["POST"],
)
@register_book_verify_route(bp.name)
@login_required
def section_edit(
    book_id: int,
    collection_id: int,
    section_id: int,
    sub_collection_id: int | None = None,
):
    redirect_url = url_for(
        "book.interpretation_view",
        book_id=book_id,
        collection_id=collection_id,
        sub_collection_id=sub_collection_id,
        section_id=section_id,
    )
    section: m.Section = db.session.get(m.Section, section_id)

    form = f.EditSectionForm()

    if form.validate_on_submit():
        label = form.label.data
        if label:
            section.label = label

        about = form.about.data
        if about:
            section.about = about

        log(log.INFO, "Edit section [%s]", section.id)
        section.save()

        flash("Success!", "success")
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Section edit errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(redirect_url)


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:section_id>/delete_section",
    methods=["POST"],
)
@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/<int:section_id>/delete_section",
    methods=["POST"],
)
@register_book_verify_route(bp.name)
@login_required
def section_delete(
    book_id: int,
    collection_id: int,
    section_id: int,
    sub_collection_id: int | None = None,
):
    collection: m.Collection = db.session.get(
        m.Collection, sub_collection_id or collection_id
    )
    section: m.Section = db.session.get(m.Section, section_id)

    section.is_deleted = True
    delete_nested_section_entities(section)
    if not collection.active_sections:
        log(
            log.INFO,
            "Section [%s] has no active section. Set is_leaf = False",
            section.id,
        )
        collection.is_leaf = False

    log(log.INFO, "Delete section [%s]", section.id)
    section.save()

    flash("Success!", "success")
    return redirect(
        url_for(
            "book.collection_view",
            book_id=book_id,
        )
    )
