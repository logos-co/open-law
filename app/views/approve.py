from flask import (
    Blueprint,
    jsonify,
)
from flask_login import login_required, current_user

from app import models as m, db
from app.logger import log

bp = Blueprint("approve", __name__, url_prefix="/approve")


@bp.route(
    "/interpretation/<int:interpretation_id>",
    methods=["POST"],
)
@login_required
def approve_interpretation(interpretation_id: int):
    interpretation: m.Interpretation = db.session.get(
        m.Interpretation, interpretation_id
    )
    if not interpretation:
        log(log.WARNING, "Interpretation with id [%s] not found", interpretation_id)
        return jsonify({"message": "Interpretation not found"}), 404

    # TODO check permission
    if interpretation.book.owner != current_user:
        log(
            log.WARNING,
            "User [%s] dont have permission to approve [%s]",
            current_user,
            interpretation,
        )
        return jsonify({"message": "You dont have permission"}), 404

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
    interpretation.save()

    return jsonify({"message": "success", "approve": interpretation.approved})


@bp.route(
    "/comment/<int:interpretation_id>",
    methods=["POST"],
)
@login_required
def approve_comment(interpretation_id: int):
    comment: m.Comment = db.session.get(m.Comment, interpretation_id)
    if not comment:
        log(log.WARNING, "Comment with id [%s] not found", interpretation_id)
        return jsonify({"message": "Comment not found"}), 404

    # TODO check permission
    if comment.interpretation.book.owner != current_user:
        log(
            log.WARNING,
            "User [%s] dont have permission to approve [%s]",
            current_user,
            comment,
        )
        return jsonify({"message": "You dont have permission"}), 404

    comment.approved = not comment.approved
    log(
        log.INFO,
        "User [%s]. [%s] comment: [%s]",
        current_user,
        "Approve" if comment.approved else "Cancel approve",
        comment,
    )
    comment.save()

    return jsonify({"message": "success", "approve": comment.approved})
