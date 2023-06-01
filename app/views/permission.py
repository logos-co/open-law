from flask import redirect, url_for, Blueprint, flash
from flask_login import current_user

from app import forms as f, models as m, db
from app.logger import log

bp = Blueprint("permission", __name__, "/permission")


@bp.route("/set", methods=["POST"])
def set():
    form: f.EditPermissionForm = f.EditPermissionForm()

    if form.validate_on_submit():
        book_id = form.book_id.data
        book: m.Book = db.session.get(m.Book, book_id)
        if not book or book.is_deleted or book.owner != current_user:
            log(log.INFO, "User: [%s] is not owner of book: [%s]", current_user, book)
            flash("You are not owner of this book!", "danger")
            return redirect(url_for("book.my_library"))

        user_id = form.user_id.data
        contributor: m.BookContributor = m.BookContributor.query.filter_by(
            user_id=user_id, book_id=book_id
        ).first()
        if not contributor:
            log(
                log.INFO,
                "User: [%s] is not contributor of book: [%s]",
                current_user,
                book,
            )
            flash("User are not contributor of this book!", "danger")
            return redirect(url_for("book.my_library"))

        # TODO process data from checkbox tree
        # permissions = json.loads(form.permissions.data)

    return {"status": "ok"}
