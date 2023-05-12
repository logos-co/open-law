from flask_login import current_user

from app import db, models as m
from app.models.utils import BaseModel


class Book(BaseModel):
    __tablename__ = "books"

    label = db.Column(db.String(256), unique=False, nullable=False)
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

    @property
    def last_version(self):
        return self.versions[-1]

    @property
    def current_user_has_star(self):
        if current_user.is_authenticated:
            book_star: m.BookStar = m.BookStar.query.filter_by(
                user_id=current_user.id, book_id=self.id
            ).first()
            if book_star:
                return True
