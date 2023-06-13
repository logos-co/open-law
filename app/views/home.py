from flask import (
    Blueprint,
    render_template,
    request,
)
from sqlalchemy import and_
from app import models as m, db
from app.logger import log
from app.controllers import create_pagination


bp = Blueprint("home", __name__, url_prefix="/home")


@bp.route("/", methods=["GET"])
def get_all():
    sort = request.args.get("sort")
    interpretations = db.session.query(
        m.Interpretation,
    ).filter(
        and_(
            m.Section.id == m.Interpretation.section_id,
            m.Collection.id == m.Section.collection_id,
            m.BookVersion.id == m.Section.version_id,
            m.Book.id == m.BookVersion.book_id,
            m.Book.is_deleted == False,  # noqa: E712
            m.BookVersion.is_deleted == False,  # noqa: E712
            m.Interpretation.is_deleted == False,  # noqa: E712
            m.Section.is_deleted == False,  # noqa: E712
            m.Collection.is_deleted == False,  # noqa: E712
        )
    )
    match sort:
        case "upvoted":
            interpretations = interpretations.order_by(m.Interpretation.score)
        case _:
            interpretations = interpretations.order_by(
                m.Interpretation.created_at.desc()
            )

    log(log.INFO, "Creating pagination for interpretations")

    pagination = create_pagination(total=interpretations.count())
    log(log.INFO, "Returns data for front end")

    log(log.INFO, "Returning data to front end")
    return render_template(
        "home/index.html",
        interpretations=interpretations.paginate(
            page=pagination.page, per_page=pagination.per_page
        ),
        page=pagination,
    )


@bp.route("/explore_books", methods=["GET"])
def explore_books():
    log(log.INFO, "Create query for home page for books")

    books: m.Book = m.Book.query.filter_by(is_deleted=False).order_by(m.Book.id)
    log(log.INFO, "Creating pagination for books")

    pagination = create_pagination(total=books.count())
    log(log.INFO, "Returns data for front end")

    return render_template(
        "home/explore_books.html",
        books=books.paginate(page=pagination.page, per_page=pagination.per_page),
        page=pagination,
    )
