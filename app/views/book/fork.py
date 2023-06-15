from flask import flash, redirect, url_for
from flask_login import login_required

from app import models as m, db, forms as f
from app.controllers.fork import fork_book
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
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(redirect_url)
