from flask import flash, redirect, url_for
from flask_login import login_required, current_user

from app.controllers import (
    register_book_verify_route,
)

from app import models as m, db, forms as f
from app.controllers.version import create_new_version
from app.controllers.delete_nested_book_entities import delete_nested_version_entities
from app.controllers.error_flashes import create_error_flash
from app.logger import log
from .bp import bp


@bp.route("/<int:book_id>/create_version", methods=["POST"])
@login_required
def create_version(book_id):
    form: f.CreateVersionForm = f.CreateVersionForm()

    redirect_url = url_for("book.settings", selected_tab="versions", book_id=book_id)
    if form.validate_on_submit():
        book = db.session.get(m.Book, book_id)
        if book.user_id != current_user.id:
            flash("You are not owner of this book", "warning")
            return redirect(redirect_url)
        create_new_version(book, form.semver.data)
        flash("Success!", "success")
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Create version errors: [%s]", form.errors)
        create_error_flash(form)
        return redirect(redirect_url)


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
        log(log.ERROR, "Edit version errors: [%s]", form.errors)
        create_error_flash(form)
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

        version.is_deleted = True
        delete_nested_version_entities(version)
        log(log.INFO, "Delete version [%s]", version)
        version.save()

        flash("Success!", "success")
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Delete version errors: [%s]", form.errors)
        create_error_flash(form)
        return redirect(redirect_url)
