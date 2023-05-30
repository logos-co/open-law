from flask import flash, redirect, url_for, current_app
from flask_login import login_required, current_user

from app.controllers import (
    register_book_verify_route,
)
from app.controllers.delete_nested_book_entities import (
    delete_nested_comment_entities,
)
from app import models as m, db, forms as f
from app.controllers.tags import set_comment_tags
from app.logger import log
from .bp import bp


@bp.route(
    "/<int:book_id>/<int:interpretation_id>/create_comment",
    methods=["POST"],
)
@login_required
def create_comment(
    book_id: int,
    interpretation_id: int,
):
    book: m.Book = db.session.get(m.Book, book_id)
    if not book or book.is_deleted:
        log(log.INFO, "User: [%s] is not owner of book: [%s]", current_user, book)
        flash("You are not owner of this book!", "danger")
        return redirect(url_for("book.my_library"))
    redirect_url = url_for(
        "book.qa_view", book_id=book_id, interpretation_id=interpretation_id
    )

    interpretation: m.Interpretation = db.session.get(
        m.Interpretation, interpretation_id
    )
    if not interpretation or interpretation.is_deleted:
        log(log.WARNING, "Interpretation with id [%s] not found", interpretation_id)
        flash("Interpretation not found", "danger")
        return redirect(redirect_url)

    form = f.CreateCommentForm()

    if form.validate_on_submit():
        text = form.text.data
        comment: m.Comment = m.Comment(
            text=text,
            user_id=current_user.id,
            interpretation_id=interpretation_id,
        )
        if form.parent_id.data:
            comment.parent_id = form.parent_id.data
            comment.interpretation = None

        log(
            log.INFO,
            "Create comment for interpretation [%s].",
            interpretation,
        )
        comment.save()

        tags = current_app.config["TAG_REGEX"].findall(text)
        set_comment_tags(comment, tags)

        flash("Success!", "success")
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Comment create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.lower().replace("field", field_label).title(), "danger")

        return redirect(redirect_url)


@bp.route("/<int:book_id>/<int:interpretation_id>/comment_delete", methods=["POST"])
@register_book_verify_route(bp.name)
@login_required
def comment_delete(book_id: int, interpretation_id: int):
    redirect_url = url_for(
        "book.qa_view", book_id=book_id, interpretation_id=interpretation_id
    )
    form = f.DeleteCommentForm()
    comment_id = form.comment_id.data
    comment: m.Comment = db.session.get(m.Comment, comment_id)

    if form.validate_on_submit():
        comment.is_deleted = True
        delete_nested_comment_entities(comment)
        log(log.INFO, "Delete comment [%s]", comment)
        comment.save()

        flash("Success!", "success")
        return redirect(redirect_url)
    flash("Invalid id!", "danger")
    return redirect(
        url_for(
            "book.collection_view",
            book_id=book_id,
        )
    )


@bp.route(
    "/<int:book_id>/<int:interpretation_id>/comment_edit",
    methods=["POST"],
)
@register_book_verify_route(bp.name)
@login_required
def comment_edit(
    book_id: int,
    interpretation_id: int,
):
    redirect_url = url_for(
        "book.qa_view", book_id=book_id, interpretation_id=interpretation_id
    )
    form = f.EditCommentForm()

    if form.validate_on_submit():
        text = form.text.data
        comment_id = form.comment_id.data
        comment: m.Comment = db.session.get(m.Comment, comment_id)
        comment.text = text
        comment.edited = True
        log(log.INFO, "Edit comment [%s]", comment)

        tags = current_app.config["TAG_REGEX"].findall(text)
        set_comment_tags(comment, tags)

        comment.save()

        flash("Success!", "success")
        return redirect(redirect_url)
    flash("Invalid id!", "danger")

    return redirect(
        url_for(
            "book.collection_view",
            book_id=book_id,
        )
    )
