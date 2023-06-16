from flask import flash, redirect, url_for
from flask_login import login_required

from app import models as m, db, forms as f
from app.controllers.fork import fork_book, fork_version
from app.controllers.error_flashes import create_error_flash
from app.logger import log
from .bp import bp


@bp.route("/<int:book_id>/fork", methods=["POST"])
@login_required
def fork(book_id):
    form: f.ForkBookForm = f.ForkBookForm()

    book = db.session.get(m.Book, book_id)
    redirect_url = url_for("book.statistic_view", book_id=book.id, active_tab="forks")
    if form.validate_on_submit():
        fork_book(book, form.label.data, form.about.data)
        flash("Success!", "success")
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Fork book errors: [%s]", form.errors)
        create_error_flash(form)
        return redirect(redirect_url)


@bp.route("/<int:book_id>/fork_version", methods=["POST"])
@login_required
def fork_specific_version(book_id):
    form: f.ForkVersionForm = f.ForkVersionForm()

    book = db.session.get(m.Book, book_id)
    redirect_url = url_for("book.statistic_view", book_id=book.id, active_tab="forks")
    if form.validate_on_submit():
        book_version: m.BookVersion = db.session.get(
            m.BookVersion, form.version_id.data
        )
        if not book_version or book_version.book_id != book_id:
            flash("Invalid version data", "warning")
        else:
            fork_version(book, form.label.data, form.about.data, book_version)
            flash("Success!", "success")
        return redirect(redirect_url)
    else:
        log(log.ERROR, "Fork book errors: [%s]", form.errors)
        create_error_flash(form)
        return redirect(redirect_url)
