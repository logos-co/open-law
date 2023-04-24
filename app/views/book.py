from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from app import models as m
from app import forms as f
from app.logger import log

bp = Blueprint("book", __name__, url_prefix="/book")


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
    form = f.CreateBookForm()
    if form.validate_on_submit():
        book = m.Book(
            label=form.label.data,
        )
        log(log.INFO, "Form submitted. Book: [%s]", book)
        flash("Book added!", "success")
        book.save()
        return redirect(url_for("book.get_all"))
    else:
        log(log.ERROR, "Book create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(url_for("book.get_all"))
