from flask import (
    Blueprint,
    jsonify,
)
from flask_login import login_required, current_user

from app import models as m, db
from app.logger import log

bp = Blueprint("star", __name__, url_prefix="/star")


@bp.route(
    "/<int:book_id>",
    methods=["POST"],
)
@login_required
def star_book(book_id: int):
    book: m.Book = db.session.get(m.Book, book_id)
    if not book:
        log(log.WARNING, "Book with id [%s] not found", book_id)
        return jsonify({"message": "Book not found"}), 404

    book_star: m.BookStar = m.BookStar.query.filter_by(
        user_id=current_user.id, book_id=book_id
    ).first()
    current_user_star = True
    if book_star:
        current_user_star = False
        db.session.delete(book_star)
        db.session.commit()
    else:
        book_star = m.BookStar(user_id=current_user.id, book_id=book_id)
        log(
            log.INFO,
            "User [%s]. Add book [%s] star",
            current_user,
            book,
        )
        book_star.save()

    return jsonify(
        {
            "stars_count": len(book.stars),
            "current_user_star": current_user_star,
        }
    )
