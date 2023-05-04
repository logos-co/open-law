from flask import (
    Blueprint,
    render_template,
)
from flask_login import current_user

from app import models as m

bp = Blueprint("home", __name__, url_prefix="/home")


@bp.route("/", methods=["GET"])
def get_all():
    books: m.Book = m.Book.query.order_by(m.Book.id).limit(5)
    sections: m.Section = m.Section.query.order_by(m.Section.id).limit(5)
    last_user_sections = []
    if current_user.is_authenticated:
        last_user_sections: m.Section = m.Section.query.order_by(
            m.Section.created_at
        ).limit(5)

    return render_template(
        "home/index.html",
        books=books,
        sections=sections,
        last_user_sections=last_user_sections,
    )
