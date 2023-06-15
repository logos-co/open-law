from flask import (
    Blueprint,
    render_template,
    request,
)
from sqlalchemy import and_, func
from app import models as m, db
from app.logger import log
from app.controllers.sorting import sort_by


bp = Blueprint("home", __name__, url_prefix="/home")


@bp.route("/", methods=["GET"])
def get_all():
    sort = request.args.get("sort")
    interpretations = (
        db.session.query(
            m.Interpretation,
            m.Interpretation.score.label("score"),
            m.Interpretation.created_at.label("created_at"),
            func.count(m.Comment.interpretation_id).label("comments_count"),
        )
        .join(
            m.Comment,
            and_(
                m.Comment.interpretation_id == m.Interpretation.id,
                m.Comment.is_deleted == False,  # noqa: E712
            ),
            isouter=True,
        )
        .filter(
            m.Interpretation.is_deleted == False,  # noqa: E712
        )
        .group_by(m.Interpretation.id)
    )
    pagination, interpretations = sort_by(interpretations, sort)

    return render_template(
        "home/index.html",
        interpretations=interpretations,
        page=pagination,
    )


@bp.route("/explore_books", methods=["GET"])
def explore_books():
    log(log.INFO, "Create query for home page for books")
    sort = request.args.get("sort")

    books: m.Book = (
        db.session.query(
            m.Book,
            m.Book.created_at.label("created_at"),
            func.count(m.Interpretation.id).label("interpretations_count"),
            func.count(m.BookStar.id).label("stars_count"),
        )
        .join(
            m.BookStar,
            and_(
                m.BookStar.book_id == m.Book.id,
                m.BookStar.is_deleted == False,  # noqa: E712
            ),
            full=True,
        )
        .join(
            m.BookVersion,
            and_(
                m.BookVersion.book_id == m.Book.id,
                m.BookVersion.is_deleted == False,  # noqa: E712
            ),
        )
        .join(
            m.Section,
            and_(
                m.BookVersion.id == m.Section.version_id,
                m.Section.is_deleted == False,  # noqa: E712
            ),
            full=True,
        )
        .join(
            m.Interpretation,
            and_(
                m.Interpretation.section_id == m.Section.id,
                m.Interpretation.is_deleted == False,  # noqa: E712
            ),
            full=True,
        )
        .filter(
            m.Book.is_deleted == False,  # noqa: E712
        )
        .group_by(m.Book.id)
    )
    log(log.INFO, "Creating pagination for books")
    pagination, books = sort_by(books, sort)
    return render_template(
        "home/explore_books.html",
        books=books,
        page=pagination,
    )
