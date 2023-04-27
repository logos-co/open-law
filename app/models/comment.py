from app import db
from app.models.utils import BaseModel


class Comment(BaseModel):
    __tablename__ = "comments"

    # need to redeclare id to use it in the parent relationship
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, unique=False, nullable=False)
    marked = db.Column(db.Boolean, default=False)
    included_with_interpretation = db.Column(db.Boolean, default=False)

    # Foreign keys
    user_id = db.Column(db.ForeignKey("users.id"))
    parent_id = db.Column(db.ForeignKey("comments.id"))
    interpretation_id = db.Column(db.ForeignKey("interpretations.id"))

    # Relationships
    user = db.relationship("User")
    children = db.relationship(
        "Comment", backref=db.backref("parent", remote_side=[id]), viewonly=True
    )
    interpretation = db.relationship("Interpretation")
    votes = db.relationship("CommentVote")
    tags = db.relationship(
        "Tag",
        secondary="comment_tags",
        back_populates="comments",
    )

    def __repr__(self):
        return f"<{self.id}: {self.text[:20]}>"
