from flask import Blueprint, render_template
from flask_login import login_required, current_user


from app.controllers import (
    create_pagination,
)


from app import models as m
from app.logger import log

bp = Blueprint("notifications", __name__, url_prefix="/notifications")


@bp.route("/all", methods=["GET"])
@login_required
def get_all():
    log(log.INFO, "Create query for notifications")
    notifications: m.Notification = m.Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(m.Notification.created_at.desc())
    log(log.INFO, "Create pagination for books")

    pagination = create_pagination(total=notifications.count())
    log(log.INFO, "Returning data for front end")

    return render_template(
        "notifications/index.html",
        notifications=notifications.paginate(
            page=pagination.page, per_page=pagination.per_page
        ),
        page=pagination,
    )

@bp.route('/mark_as_read',methods=["GET"])
@login_required
def mark_as_read():
    