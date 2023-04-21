from app import db
from app.models.utils import BaseModel


class CommentTags(BaseModel):
    __tablename__ = "comment_tags"

    # Foreign keys
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"))

    def __repr__(self):
        return f"<t:{self.tag} to c:{self.comment}"
