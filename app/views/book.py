from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    request,
)
from flask_login import login_required

from app import models as m
from app import forms as f
from app.logger import log
from app.controllers import create_pagination

bp = Blueprint("book", __name__, url_prefix="/book")


@bp.route("/", methods=["GET"])
def get_all():
    q = request.args.get("q", type=str, default=None)
    books = m.Book.query.order_by(m.Book.id)
    if q:
        books = books.filter(m.Book.label.like(f"{q}"))

    pagination = create_pagination(total=books.count())

    return render_template(
        "book/index.html",
        books=books.paginate(page=pagination.page, per_page=pagination.per_page),
        page=pagination,
        search_query=q,
    )


@bp.route("/create", methods=["POST"])
@login_required
def create():
    form = f.NewBookForm()
    if form.validate_on_submit():
        book = m.Book(
            label=form.label.data,
        )
        log(log.INFO, "Form submitted. User: [%s]", book)
        flash("Book added!", "success")
        book.save()
        return redirect(url_for("book.get_all"))


@bp.route("/<int:book_id>", methods=["GET"])
@login_required
def view(book_id):
    b = m.Book.query.filter_by(id=book_id).first()
    if not b:
        log(log.CRITICAL, "Book with id [%s] not found", book_id)
        flash("Book not found", "danger")
        return redirect(url_for("book.get_all"))
    else:
        return render_template("book/view.html", book=b)
