from flask import (
    Blueprint,
    render_template,
    request,
)

from app.controllers import create_pagination
from app import models as m


bp = Blueprint("section", __name__, url_prefix="/section")


@bp.route("/all", methods=["GET"])
def get_all():
    q = request.args.get("q", type=str, default=None)
    section: m.Section = m.Section.query.order_by(m.Section.id)
    if q:
        section = section.filter(m.Section.label.like(f"{q}"))

    pagination = create_pagination(total=section.count())

    return render_template(
        "section/all.html",
        sections=section.paginate(page=pagination.page, per_page=pagination.per_page),
        page=pagination,
        search_query=q,
        all_books=True,
    )
