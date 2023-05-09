from flask import (
    Blueprint,
    jsonify,
)
from flask_login import login_required, current_user

from app import models as m, db, forms as f
from app.logger import log

bp = Blueprint("vote", __name__, url_prefix="/vote")


@bp.route(
    "/interpretation/<int:interpretation_id>",
    methods=["POST"],
)
@login_required
def vote_interpretation(interpretation_id: int):
    interpretation: m.Interpretation = db.session.get(
        m.Interpretation, interpretation_id
    )
    if not interpretation:
        log(log.WARNING, "Interpretation with id [%s] not found", interpretation_id)
        return jsonify({"message": "Interpretation not found"}), 404

    form = f.VoteForm()
    if form.validate_on_submit():
        vote: m.InterpretationVote = m.InterpretationVote.query.filter_by(
            user_id=current_user.id, interpretation_id=interpretation_id
        ).first()
        if vote:
            db.session.delete(vote)

        positive = form.positive.data and "True" in form.positive.raw_data
        if not vote or vote.positive != positive:
            vote: m.InterpretationVote = m.InterpretationVote(
                user_id=current_user.id,
                interpretation_id=interpretation_id,
                positive=positive,
            )
            log(
                log.INFO,
                "User [%s]. [%s] vote interpretation: [%s]",
                current_user,
                "Positive" if positive else "Negative",
                interpretation,
            )
            vote.save(False)
        else:
            log(
                log.INFO,
                "User [%s]. Remove [%s] vote for interpretation: [%s]",
                current_user,
                "positive" if positive else "negative",
                interpretation,
            )
        db.session.commit()

        return jsonify({"vote_count": interpretation.vote_count})

    log(
        log.CRITICAL,
        "Unexpected error: User [%s]. Vote for interpretation: [%s]",
        current_user,
        interpretation,
    )
    return jsonify({"message": "Unexpected error"}), 400
