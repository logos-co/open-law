from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from sqlalchemy import and_, or_

from app.controllers import (
    create_pagination,
    register_book_verify_route,
)
from app.controllers.tags import (
    set_book_tags,
)
from app.controllers.delete_nested_book_entities import (
    delete_nested_book_entities,
)
from app.controllers.create_access_groups import (
    create_editor_group,
    create_moderator_group,
)
from app.controllers.require_permission import require_permission
from app import models as m, db, forms as f
from app.logger import log
from .bp import bp


# @bp.route("/all", methods=["GET"])
# def get_all():
#     log(log.INFO, "Create query for books")
#     books: m.Book = m.Book.query.filter(m.Book.is_deleted is not False).order_by(
#         m.Book.id
#     )
#     log(log.INFO, "Create pagination for books")

#     pagination = create_pagination(total=books.count())
#     log(log.INFO, "Returning data for front end")

#     return render_template(
#         "book/all.html",
#         books=books.paginate(page=pagination.page, per_page=pagination.per_page),
#         page=pagination,
#         all_books=True,
#     )


@bp.route("/create_version", methods=["POST"])
@login_required
def create_version():
    raise NotImplementedError


@bp.route("/<int:book_id>/edit_version", methods=["POST"])
@register_book_verify_route(bp.name)
@login_required
def edit_version(book_id: int):
    form: f.EditVersionForm = f.EditVersionForm()

    redirect_url = url_for("book.settings", selected_tab="versions", book_id=book_id)

    if form.validate_on_submit():
        semver = form.semver.data
        version_id = form.version_id.data

        book: m.Book = db.session.get(m.Book, book_id)
        version: m.BookVersion = db.session.get(m.BookVersion, version_id)
        if book.user_id != current_user.id:
            flash("You are not owner of this book", "warning")
            return redirect(redirect_url)
        elif version.book.id != book_id:
            flash("Invalid version id", "warning")
            return redirect(redirect_url)

        version.semver = semver
        log(log.INFO, "Edit version [%s]", version)
        version.save()

        flash("Success!", "success")
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Section edit errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(redirect_url)


@bp.route("/<int:book_id>/delete_version", methods=["POST"])
@login_required
def delete_version(book_id: int):
    form: f.DeleteVersionForm = f.DeleteVersionForm()

    redirect_url = url_for("book.settings", selected_tab="versions", book_id=book_id)

    if form.validate_on_submit():
        version_id = form.version_id.data

        book: m.Book = db.session.get(m.Book, book_id)
        version: m.BookVersion = db.session.get(m.BookVersion, version_id)
        if book.user_id != current_user.id:
            flash("You are not owner of this book", "warning")
            return redirect(redirect_url)
        elif version.book.id != book_id:
            flash("Invalid version id", "warning")
            return redirect(redirect_url)
        elif version.is_active:
            flash("You cant delete active version", "warning")
            return redirect(redirect_url)

        # TODO delete nested items
        # log(log.INFO, "Edit version [%s]", version)
        # version.save()

        flash("Success!", "success")
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Section edit errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(redirect_url)
