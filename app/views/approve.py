from flask import (
    Blueprint,
    jsonify,
)
from flask_login import login_required, current_user

from app import models as m, db
from app.controllers.notification_producer import (
    interpretation_notification,
    comment_notification,
)
from app.controllers.require_permission import require_permission
from app.logger import log

bp = Blueprint("approve", __name__, url_prefix="/approve")


@bp.route(
    "/interpretation/<int:interpretation_id>",
    methods=["POST"],
)
@require_permission(
    entity_type=m.Permission.Entity.INTERPRETATION,
    access=[m.Permission.Access.A],
    entities=[m.Interpretation],
)
@login_required
def approve_interpretation(interpretation_id: int):
    interpretation: m.Interpretation = db.session.get(
        m.Interpretation, interpretation_id
    )
    book: m.Book = db.session.get(m.Book, interpretation.book.id)
    if not interpretation:
        log(log.WARNING, "Interpretation with id [%s] not found", interpretation_id)
        return jsonify({"message": "Interpretation not found"}), 404

    already_approved_interpretations = (
        m.Interpretation.query.filter_by(
            approved=True, section_id=interpretation.section_id
        )
        .filter(m.Interpretation.id != interpretation.id)
        .all()
    )
    for approved_interpretation in already_approved_interpretations:
        approved_interpretation: m.Interpretation
        approved_interpretation.approved = False
        log(
            log.INFO,
            "User [%s] revoked the approval of the interpretation: [%s]",
            current_user,
            interpretation,
        )
        approved_interpretation.save(False)

    interpretation.approved = not interpretation.approved
    log(
        log.INFO,
        "User [%s]. [%s] interpretation: [%s]",
        current_user,
        "Approve" if interpretation.approved else "Cancel approve",
        interpretation,
    )
    if interpretation.approved and current_user.id != interpretation.user_id:
        # notifications
        interpretation_notification(
            m.Notification.Actions.APPROVE, interpretation.id, book.owner.id
        )
        interpretation_notification(
            m.Notification.Actions.APPROVE, interpretation.id, interpretation.user_id
        )

    interpretation.save()

    return jsonify({"message": "success", "approve": interpretation.approved})


@bp.route(
    "/comment/<int:comment_id>",
    methods=["POST"],
)
@require_permission(
    entity_type=m.Permission.Entity.COMMENT,
    access=[m.Permission.Access.A],
    entities=[m.Comment],
)
@login_required
def approve_comment(comment_id: int):
    comment: m.Comment = db.session.get(m.Comment, comment_id)
    book: m.Book = db.session.get(m.Book, comment.book.id)
    if not comment:
        log(log.WARNING, "Comment with id [%s] not found", comment_id)
        return jsonify({"message": "Comment not found"}), 404

    comment.approved = not comment.approved
    log(
        log.INFO,
        "User [%s]. [%s] comment: [%s]",
        current_user,
        "Approve" if comment.approved else "Cancel approve",
        comment,
    )
    # TODO:refactor if
    if (
        comment.approved
        and current_user.id != comment.book.owner.id
        and current_user.id != comment.user_id
    ):
        # notifications
        comment_notification(m.Notification.Actions.APPROVE, comment.id, book.owner.id)
    elif comment.approved and current_user.id != comment.user_id:
        # Your interpretation has been approved for SectionLabel on BookLabel
        comment_notification(
            m.Notification.Actions.APPROVE, comment.id, comment.user_id
        )
        # -------------
    comment.save()

    return jsonify({"message": "success", "approve": comment.approved})
