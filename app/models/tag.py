from app import db
from app.models.utils import BaseModel


class Tag(BaseModel):
    __tablename__ = "tags"

    name = db.Column(db.String(32), unique=True, nullable=False)

    # Relationships
    interpretations = db.relationship(
        "Interpretation", secondary="interpretation_tags", back_populates="tags"
    )
    comments = db.relationship(
        "Comment", secondary="comment_tags", back_populates="tags"
    )

    def __repr__(self):
        return f"<{self.id}: {self.name}>"
