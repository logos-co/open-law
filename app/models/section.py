from app import db
from app.models.utils import BaseModel


class Section(BaseModel):
    __tablename__ = "sections"

    label = db.Column(db.String(1024), unique=False, nullable=False)
    about = db.Column(db.Text, unique=False, nullable=False)

    # Foreign keys
    collection_id = db.Column(db.ForeignKey("collections.id"))
    user_id = db.Column(db.ForeignKey("users.id"))

    # Relationships
    collection = db.relationship("Collection", viewonly=True)
    user = db.relationship("User")

    def __repr__(self):
        return f"<{self.id}: {self.label}>"
