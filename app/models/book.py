from app import db
from app.models.utils import BaseModel


class Book(BaseModel):
    __tablename__ = "books"

    label = db.Column(db.String(1024), unique=False, nullable=False)
    about = db.Column(db.Text, unique=False, nullable=True)

    # Foreign keys
    user_id = db.Column(db.ForeignKey("users.id"))

    # Relationships
    owner = db.relationship("User", viewonly=True)
    stars = db.relationship("User", secondary="books_stars", back_populates="stars")
    contributors = db.relationship("BookContributor")
    versions = db.relationship("BookVersion")

    def __repr__(self):
        return f"<{self.id}: {self.label}>"
