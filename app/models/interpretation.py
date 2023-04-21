from app import db
from app.models.utils import BaseModel


class Interpretation(BaseModel):
    __tablename__ = "interpretations"

    label = db.Column(db.String(1024), unique=False, nullable=False)
    about = db.Column(db.Text, unique=False, nullable=False)
    marked = db.Column(db.Boolean, default=False)

    # Foreign keys
    user_id = db.Column(db.ForeignKey("users.id"))
    section_id = db.Column(db.ForeignKey("sections.id"))

    # Relationships
    user = db.relationship("User")
    section = db.relationship("Section")
    comments = db.relationship("Comment", viewonly=True)
    votes = db.relationship("InterpretationVote", viewonly=True)
    tags = db.relationship(
        "Tag",
        secondary="interpretation_tags",
        back_populates="interpretations",
    )

    def __repr__(self):
        return f"<{self.id}: {self.label}>"
