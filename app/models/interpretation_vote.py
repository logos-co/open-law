from app import db
from app.models.utils import BaseModel


class InterpretationVote(BaseModel):
    __tablename__ = "interpretation_votes"

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    interpretation_id = db.Column(db.Integer, db.ForeignKey("interpretations.id"))
    possitive = db.Column(db.Boolean, default=True)

    # Relationships
    user = db.relationship("User", viewonly=True)
    interpretation = db.relationship("Interpretation", viewonly=True)

    def __repr__(self):
        return f"<{self.user} to {self.interpretation} Positive:{self.possitive}>"
