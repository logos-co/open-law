from app import db
from app.models.utils import BaseModel


class BookStar(BaseModel):
    __tablename__ = "books_stars"

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))

    # Relationships
    user = db.relationship("User", viewonly=True)
    book = db.relationship("Book", viewonly=True)

    def __repr__(self):
        return f"<{self.user} to {self.book}>"
