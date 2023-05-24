from flask import (
    Blueprint,
    render_template,
)
from sqlalchemy import and_
from app import models as m, db

bp = Blueprint("home", __name__, url_prefix="/home")


@bp.route("/", methods=["GET"])
def get_all():
    books: m.Book = (
        m.Book.query.filter_by(is_deleted=False).order_by(m.Book.id).limit(5)
    ).all()
    interpretations = (
        db.session.query(
            m.Interpretation,
        )
        .filter(
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
        .order_by(m.Interpretation.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "home/index.html",
        books=books,
        interpretations=interpretations,
    )
