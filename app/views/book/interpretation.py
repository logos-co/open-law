from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    current_app,
)
from flask_login import login_required, current_user

from app.controllers import register_book_verify_route, create_breadcrumbs, clean_html
from app.controllers.delete_nested_book_entities import (
    delete_nested_interpretation_entities,
)
from app import models as m, db, forms as f
from app.controllers.tags import set_interpretation_tags
from app.logger import log
from .bp import bp


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:section_id>/interpretations",
    methods=["GET"],
)
@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/<int:section_id>/interpretations",
    methods=["GET"],
)
def interpretation_view(
    book_id: int,
    collection_id: int,
    section_id: int,
    sub_collection_id: int | None = None,
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

    section: m.Section = db.session.get(m.Section, section_id)
    if not section:
        log(log.WARNING, "Section with id [%s] not found", section_id)
        flash("Section not found", "danger")
        return redirect(
            url_for(
                "book.section_view",
                book_id=book_id,
                collection_id=collection_id,
                sub_collection_id=sub_collection_id,
            )
        )
    else:
        breadcrumbs = create_breadcrumbs(
            book_id=book_id,
            collection_path=(
                collection_id,
                sub_collection_id,
            ),
            section_id=section_id,
        )
        return render_template(
            "book/interpretation_view.html",
            book=book,
            collection=collection,
            sub_collection=sub_collection if sub_collection_id else None,
            section=section,
            breadcrumbs=breadcrumbs,
        )


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:section_id>/create_interpretation",
    methods=["POST"],
)
@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/<int:section_id>/create_interpretation",
    methods=["POST"],
)
@register_book_verify_route(bp.name)
@login_required
def interpretation_create(
    book_id: int,
    collection_id: int,
    section_id: int,
    sub_collection_id: int | None = None,
):
    section: m.Section = db.session.get(m.Section, section_id)
    form = f.CreateInterpretationForm()
    redirect_url = url_for(
        "book.interpretation_view",
        book_id=book_id,
        collection_id=collection_id,
        sub_collection_id=sub_collection_id,
        section_id=section.id,
    )

    if form.validate_on_submit():
        text = form.text.data
        plain_text = clean_html(text).lower()
        tags = current_app.config["TAG_REGEX"].findall(text)
        for tag in tags:
            word = tag.lower().replace("[", "").replace("]", "")
            plain_text = plain_text.replace(tag.lower(), word)

        interpretation: m.Interpretation = m.Interpretation(
            plain_text=plain_text,
            text=text,
            section_id=section_id,
            user_id=current_user.id,
        )
        log(
            log.INFO,
            "Create interpretation [%s]. Section: [%s]",
            interpretation,
            section,
        )
        interpretation.save()

        # access groups
        for access_group in interpretation.section.access_groups:
            m.InterpretationAccessGroups(
                interpretation_id=interpretation.id, access_group_id=access_group.id
            ).save()
        # -------------

        tags = current_app.config["TAG_REGEX"].findall(text)
        set_interpretation_tags(interpretation, tags)

        flash("Success!", "success")
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Interpretation create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(redirect_url)


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:section_id>/<int:interpretation_id>/edit_interpretation",
    methods=["POST"],
)
@bp.route(
    (
        "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/"
        "<int:section_id>/<int:interpretation_id>/edit_interpretation"
    ),
    methods=["POST"],
)
@register_book_verify_route(bp.name)
@login_required
def interpretation_edit(
    book_id: int,
    collection_id: int,
    section_id: int,
    interpretation_id: int,
    sub_collection_id: int | None = None,
):
    interpretation: m.Interpretation = db.session.get(
        m.Interpretation, interpretation_id
    )
    form = f.EditInterpretationForm()
    redirect_url = url_for(
        "book.qa_view",
        book_id=book_id,
        collection_id=collection_id,
        sub_collection_id=sub_collection_id,
        section_id=section_id,
        interpretation_id=interpretation_id,
    )

    if form.validate_on_submit():
        text = form.text.data
        plain_text = clean_html(text).lower()
        tags = current_app.config["TAG_REGEX"].findall(text)
        for tag in tags:
            word = tag.lower().replace("[", "").replace("]", "")
            plain_text = plain_text.replace(tag.lower(), word)

        interpretation.plain_text = plain_text
        interpretation.text = text
        tags = current_app.config["TAG_REGEX"].findall(text)
        set_interpretation_tags(interpretation, tags)

        log(log.INFO, "Edit interpretation [%s]", interpretation.id)
        interpretation.save()

        flash("Success!", "success")
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Interpretation edit errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(redirect_url)


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:section_id>/<int:interpretation_id>/delete_interpretation",
    methods=["POST"],
)
@bp.route(
    (
        "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/"
        "<int:section_id>/<int:interpretation_id>/delete_interpretation"
    ),
    methods=["POST"],
)
@register_book_verify_route(bp.name)
@login_required
def interpretation_delete(
    book_id: int,
    collection_id: int,
    section_id: int,
    interpretation_id: int,
    sub_collection_id: int | None = None,
):
    interpretation: m.Interpretation = db.session.get(
        m.Interpretation, interpretation_id
    )

    interpretation.is_deleted = True
    delete_nested_interpretation_entities(interpretation)

    log(log.INFO, "Delete interpretation [%s]", interpretation)
    interpretation.save()

    flash("Success!", "success")
    return redirect(
        url_for(
            "book.collection_view",
            book_id=book_id,
        )
    )


@bp.route(
    "/<int:book_id>/<int:collection_id>/<int:section_id>/<int:interpretation_id>/preview",
    methods=["GET"],
)
@bp.route(
    (
        "/<int:book_id>/<int:collection_id>/<int:sub_collection_id>/"
        "<int:section_id>/<int:interpretation_id>/preview"
    ),
    methods=["GET"],
)
def qa_view(
    book_id: int,
    collection_id: int,
    section_id: int,
    interpretation_id: int,
    sub_collection_id: int | None = None,
):
    book: m.Book = db.session.get(m.Book, book_id)
    if not book or book.is_deleted:
        log(log.INFO, "User: [%s] is not owner of book: [%s]", current_user, book)
        flash("You are not owner of this book!", "danger")
        return redirect(url_for("book.my_library"))

    collection: m.Collection = db.session.get(m.Collection, collection_id)
    if not collection or collection.is_deleted:
        log(log.WARNING, "Collection with id [%s] not found", collection_id)
        flash("Collection not found", "danger")
        return redirect(url_for("book.collection_view", book_id=book_id))

    if sub_collection_id:
        sub_collection: m.Collection = db.session.get(m.Collection, sub_collection_id)
        if not sub_collection or sub_collection.is_deleted:
            log(log.WARNING, "Sub_collection with id [%s] not found", sub_collection_id)
            flash("SubCollection not found", "danger")
            return redirect(
                url_for(
                    "book.sub_collection_view",
                    book_id=book_id,
                    collection_id=collection_id,
                )
            )

    redirect_url = url_for(
        "book.interpretation_view",
        book_id=book_id,
        collection_id=collection_id,
        sub_collection_id=sub_collection_id,
        section_id=section_id,
    )
    section: m.Section = db.session.get(m.Section, section_id)
    if not section or section.is_deleted:
        log(log.WARNING, "Section with id [%s] not found", section_id)
        flash("Section not found", "danger")
        return redirect(redirect_url)

    interpretation: m.Interpretation = db.session.get(
        m.Interpretation, interpretation_id
    )
    if not interpretation or interpretation.is_deleted:
        log(log.WARNING, "Interpretation with id [%s] not found", interpretation_id)
        flash("Interpretation not found", "danger")
        return redirect(redirect_url)

    breadcrumbs = create_breadcrumbs(
        book_id=book_id,
        collection_path=(
            collection_id,
            sub_collection_id,
        ),
        section_id=section_id,
        interpretation_id=interpretation.id,
    )
    return render_template(
        "book/qa_view.html",
        book=book,
        collection=collection,
        sub_collection=sub_collection if sub_collection_id else None,
        section=section,
        interpretation=interpretation,
        breadcrumbs=breadcrumbs,
    )
