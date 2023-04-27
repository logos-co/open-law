from app import db
from app.models.utils import BaseModel


class CommentVote(BaseModel):
    __tablename__ = "comment_votes"

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"))
    positive = db.Column(db.Boolean, default=True)

    # Relationships
    user = db.relationship("User", viewonly=True)
    comment = db.relationship("Comment", viewonly=True)

    def __repr__(self):
        return f"<{self.user} to {self.comment} Positive:{self.positive}>"
