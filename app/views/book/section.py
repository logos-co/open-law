from flask import flash, redirect, url_for, request
from flask_login import login_required, current_user

from app.controllers import register_book_verify_route
from app.controllers.delete_nested_book_entities import delete_nested_section_entities
from app import models as m, db, forms as f
from app.controllers.require_permission import require_permission
from app.logger import log
from .bp import bp


@bp.route("/<int:book_id>/<int:collection_id>/create_section", methods=["POST"])
@register_book_verify_route(bp.name)
@require_permission(
    entity_type=m.Permission.Entity.SECTION,
    access=[m.Permission.Access.C],
    entities=[m.Collection],
)
@login_required
def section_create(book_id: int, collection_id: int):
    book: m.Book = db.session.get(m.Book, book_id)
    collection: m.Collection = db.session.get(m.Collection, collection_id)

    redirect_url = url_for("book.collection_view", book_id=book_id)

    form = f.CreateSectionForm()

    if form.validate_on_submit():
        position = 0
        if collection.active_sections:
            position = len(collection.active_sections)

        section: m.Section = m.Section(
            label=form.label.data,
            collection_id=collection_id,
            version_id=book.last_version.id,
            position=position,
        )
        collection.is_leaf = True
        log(log.INFO, "Create section [%s]. Collection: [%s]", section, collection_id)
        section.save()

        # access groups
        for access_group in section.collection.access_groups:
            m.SectionAccessGroups(
                section_id=section.id, access_group_id=access_group.id
            ).save()
        # -------------

        if current_user.id != book.owner.id:
            # notifications
            notification_text = (
                f"{current_user.username} create a section on {book.label}"
            )
            m.Notification(
                link=redirect_url, text=notification_text, user_id=book.owner.id
            ).save()
            log(
                log.INFO,
                "Create notification for user with id[%s]",
                book.owner.id,
            )
        # -------------
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
@require_permission(
    entity_type=m.Permission.Entity.SECTION,
    access=[m.Permission.Access.U],
    entities=[m.Section],
)
@login_required
def section_edit(book_id: int, section_id: int):
    section: m.Section = db.session.get(m.Section, section_id)
    book: m.Book = db.session.get(m.Book, book_id)

    form = f.EditSectionForm()
    redirect_url = url_for("book.collection_view", book_id=book_id)

    if form.validate_on_submit():
        label = form.label.data
        if label:
            section.label = label

        log(log.INFO, "Edit section [%s]", section.id)
        section.save()

        if current_user.id != book.owner.id:
            # notifications
            notification_text = (
                f"{current_user.username} renamed a section on {book.label}"
            )
            m.Notification(
                link=redirect_url, text=notification_text, user_id=book.owner.id
            ).save()
            log(
                log.INFO,
                "Create notification for user with id[%s]",
                book.owner.id,
            )
            # -------------

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
@require_permission(
    entity_type=m.Permission.Entity.SECTION,
    access=[m.Permission.Access.D],
    entities=[m.Section],
)
@login_required
def section_delete(
    book_id: int,
    section_id: int,
):
    section: m.Section = db.session.get(m.Section, section_id)
    book: m.Book = db.session.get(m.Book, book_id)
    redirect_url = url_for("book.collection_view", book_id=book_id)

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

    if current_user.id != book.owner.id:
        # notifications
        notification_text = f"{current_user.username} deleted a section on {book.label}"
        m.Notification(
            link=redirect_url, text=notification_text, user_id=book.owner.id
        ).save()
        log(
            log.INFO,
            "Create notification for user with id[%s]",
            book.owner.id,
        )
        # -------------

    flash("Success!", "success")
    return redirect(redirect_url)


@bp.route("/<int:book_id>/<int:section_id>/section/change_position", methods=["POST"])
@register_book_verify_route(bp.name)
@login_required
def change_section_position(book_id: int, section_id: int):
    section: m.Section = db.session.get(m.Section, section_id)
    new_position = request.json.get("position")
    collection_id = request.json.get("collection_id")

    collection: m.Collection = section.collection
    if collection_id is not None:
        collection: m.Collection = db.session.get(m.Collection, collection_id)
        if not collection:
            log(log.INFO, "Collection with id [%s] not found", collection_id)
            return {"message": "collection not found"}, 404

        log(
            log.INFO,
            "Change section [%s] collection_id to [%s]",
            section,
            collection_id,
        )
        section.collection_id = collection_id

    if collection.active_sections:
        sections_to_edit = (
            m.Section.query.filter(
                m.Section.collection_id == collection.id,
                m.Section.id != section.id,
            )
            .order_by(m.Section.position)
            .all()
        )
        sections_to_edit.insert(new_position, section)
        log(log.INFO, "Calculate new positions of sections in [%s]", collection)
        for position in range(len(sections_to_edit)):
            sections_to_edit[position].position = position
            sections_to_edit[position].save(False)
    else:
        log(
            log.INFO,
            "Collection [%s] does not have active sections. Set section [%s] position to 1",
            collection,
            section,
        )
        section.position = 1

    log(log.INFO, "Apply position changes on [%s]", section)
    section.save()
    return {"message": "success"}
