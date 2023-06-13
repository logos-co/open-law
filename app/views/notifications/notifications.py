from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user


from app.controllers import (
    create_pagination,
)


from app import models as m, db
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


@bp.route("/<int:notification_id>/mark_as_read", methods=["GET"])
@login_required
def mark_as_read(notification_id: int):
    notification: m.Notification = db.session.get(m.Notification, notification_id)
    notification.is_read = True
    notification.save()
    return redirect(notification.link)


@bp.route("/mark_all_as_read", methods=["GET"])
@login_required
def mark_all_as_read():
    for notification in current_user.notifications:
        notification.is_read = True
        notification.save(False)
    db.session.commit()
    return redirect(url_for("notifications.get_all"))
