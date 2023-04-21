from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from flask_login import login_required
from app.controllers import create_pagination

from app import models as m
from app import forms as f
from app.logger import log

bp = Blueprint("books", __name__, url_prefix="/books")


@bp.route("/", methods=["GET"])
def get_all():
    # q = request.args.get("q", type=str, default=None)
    # books = m.Book.query.order_by(m.Book.id)
    # if q:
    #     books = books.filter(m.Book.label.like(f"{q}"))

    # pagination = create_pagination(total=books.count())

    # return render_template(
    #     "books/index.html",
    #     books=books.paginate(page=pagination.page, per_page=pagination.per_page),
    #     page=pagination,
    #     search_query=q,
    # )
    return render_template(
        "books/index.html",
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
        return redirect(url_for("books.get_all"))
