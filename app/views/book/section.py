from flask import (
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


@bp.route("/<int:book_id>/<int:collection_id>/create_section", methods=["POST"])
@register_book_verify_route(bp.name)
@login_required
def section_create(book_id: int, collection_id: int):
    book: m.Book = db.session.get(m.Book, book_id)
    collection: m.Collection = db.session.get(m.Collection, collection_id)

    redirect_url = url_for("book.collection_view", book_id=book_id)
    if collection_id:
        redirect_url = url_for(
            "book.collection_view",
            book_id=book_id,
        )

    form = f.CreateSectionForm()

    if form.validate_on_submit():
        section: m.Section = m.Section(
            label=form.label.data,
            collection_id=collection_id,
            version_id=book.last_version.id,
        )
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


@bp.route("/<int:book_id>/<int:section_id>/edit_section", methods=["POST"])
@register_book_verify_route(bp.name)
@login_required
def section_edit(book_id: int, section_id: int):
    section: m.Section = db.session.get(m.Section, section_id)

    form = f.EditSectionForm()
    redirect_url = url_for("book.collection_view", book_id=book_id)

    if form.validate_on_submit():
        label = form.label.data
        if label:
            section.label = label

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


@bp.route("/<int:book_id>/<int:section_id>/delete_section", methods=["POST"])
@register_book_verify_route(bp.name)
@login_required
def section_delete(
    book_id: int,
    section_id: int,
):
    section: m.Section = db.session.get(m.Section, section_id)

    section.is_deleted = True
    delete_nested_section_entities(section)
    if not section.collection.active_sections:
        log(
            log.INFO,
            "Section [%s] has no active section. Set is_leaf = False",
            section.id,
        )
        section.collection.is_leaf = False

    log(log.INFO, "Delete section [%s]", section.id)
    section.save()

    flash("Success!", "success")
    return redirect(url_for("book.collection_view", book_id=book_id))
