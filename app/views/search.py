from flask import Blueprint, render_template, request
from sqlalchemy import func, and_, or_

from app import models as m, db
from app.controllers import create_pagination


bp = Blueprint("search", __name__)


@bp.route("/search_interpretations", methods=["GET"])
def search_interpretations():
    q = request.args.get("q", type=str, default="").lower()
    interpretations = m.Interpretation.query.order_by(m.Interpretation.id).filter(
        (func.lower(m.Interpretation.plain_text).like(f"%{q}%"))
    )
    count = interpretations.count()
    pagination = create_pagination(total=interpretations.count())

    return render_template(
        "searchResultsInterpretations.html",
        query=q,
        interpretations=interpretations.paginate(
            page=pagination.page, per_page=pagination.per_page
        ),
        page=pagination,
        count=count,
    )


@bp.route("/search_books", methods=["GET"])
def search_books():
    q = request.args.get("q", type=str, default="")
    books = (
        db.session.query(m.Book)
        .filter(
            or_(
                and_(
                    func.lower(m.Book.label).like(f"%{q}%"),
                    m.Book.is_deleted == False,  # noqa: E712
                ),
                and_(
                    func.lower(m.Collection.label).like(f"%{q}%"),
                    m.Collection.is_deleted == False,  # noqa: E712
                    m.Collection.is_root == False,  # noqa: E712
                    m.BookVersion.id == m.Collection.version_id,
                    m.Book.id == m.BookVersion.book_id,
                    m.Book.is_deleted == False,  # noqa: E712
                ),
                and_(
                    func.lower(m.Section.label).like(f"%{q}%"),
                    m.Section.is_deleted == False,  # noqa: E712
                    m.BookVersion.id == m.Section.version_id,
                    m.Book.id == m.BookVersion.book_id,
                    m.Book.is_deleted == False,  # noqa: E712
                ),
                and_(
                    func.lower(m.Interpretation.plain_text).like(f"%{q}%"),
                    m.Interpretation.is_deleted == False,  # noqa: E712
                    m.Interpretation.section_id == m.Section.id,
                    m.Section.is_deleted == False,  # noqa: E712
                    m.BookVersion.id == m.Section.version_id,
                    m.Book.id == m.BookVersion.book_id,
                    m.Book.is_deleted == False,  # noqa: E712
                ),
            ),
        )
        .order_by(m.Book.created_at.asc())
        .group_by(m.Book.id)
    )
    count = books.count()
    pagination = create_pagination(total=books.count())

    return render_template(
        "searchResultsBooks.html",
        query=q,
        books=books.paginate(page=pagination.page, per_page=pagination.per_page),
        page=pagination,
        count=count,
    )


@bp.route("/search_users", methods=["GET"])
def search_users():
    q = request.args.get("q", type=str, default="")
    users = (
        m.User.query.order_by(m.User.id)
        .filter(
            or_(
                func.lower(m.User.username).like(f"%{q}%"),
                func.lower(m.User.wallet_id).like(f"%{q}%"),
            )
        )
        .order_by(m.User.id.asc())
        .group_by(m.User.id)
    )

    count = users.count()
    pagination = create_pagination(total=users.count())

    return render_template(
        "searchResultsUsers.html",
        query=q,
        users=users.paginate(page=pagination.page, per_page=pagination.per_page),
        page=pagination,
        count=count,
    )


@bp.route("/search_tags", methods=["GET"])
def search_tags():
    q = request.args.get("q", type=str, default="")
    tags = m.Tag.query.order_by(m.Tag.id)
    if q:
        tags = tags.filter(func.lower(m.Tag.name).like(f"%{q}%"))
    count = tags.count()
    pagination = create_pagination(total=tags.count())

    return render_template(
        "searchResultsTags.html",
        query=q,
        tags=tags.paginate(page=pagination.page, per_page=pagination.per_page),
        page=pagination,
        count=count,
    )
