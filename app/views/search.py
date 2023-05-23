from flask import Blueprint, render_template, request
from sqlalchemy import func

from app import models as m


bp = Blueprint("search", __name__)


@bp.route("/search_interpretations", methods=["GET"])
def search_interpretations():
    q = request.args.get("q", type=str, default="").lower()
    interpretations = m.Interpretation.query.order_by(m.Interpretation.id)
    if q:
        interpretations = interpretations.filter(
            (func.lower(m.Interpretation.plain_text).like(f"%{q}%"))
        )
    count = interpretations.count()

    books = m.Book.query.order_by(m.Book.id)
    if q:
        books = books.filter(m.Book.label.like(f"%{q}%"))
    return render_template(
        "searchResultsInterpretations.html",
        query=q,
        interpretations=interpretations,
        count=count,
    )


@bp.route("/search_books", methods=["GET"])
def search_books():
    q = request.args.get("q", type=str, default="")
    books = m.Book.query.order_by(m.Book.id)
    if q:
        books = books.filter((func.lower(m.Book.label).like(f"%{q}%")))
    count = books.count()

    return render_template(
        "searchResultsBooks.html",
        query=q,
        books=books,
        count=count,
    )


@bp.route("/search_users", methods=["GET"])
def search_users():
    q = request.args.get("q", type=str, default="")
    users = m.User.query.order_by(m.User.id)
    if q:
        users = users.filter(func.lower(m.User.username).like(f"%{q}%"))
    count = users.count()

    return render_template(
        "searchResultsUsers.html",
        query=q,
        users=users,
        count=count,
    )


@bp.route("/search_tags", methods=["GET"])
def search_tags():
    q = request.args.get("q", type=str, default="")
    tags = m.Tag.query.order_by(m.Tag.id)
    if q:
        tags = tags.filter(func.lower(m.Tag.name).like(f"%{q}%"))
    count = tags.count()

    return render_template(
        "searchResultsUsers.html",
        query=q,
        tags=tags,
        count=count,
    )
