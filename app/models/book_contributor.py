from enum import IntEnum

from app import db
from app.models.utils import BaseModel


class BookContributor(BaseModel):
    __tablename__ = "book_contributors"

    class Roles(IntEnum):
        UNKNOWN = 0
        MODERATOR = 1
        EDITOR = 2

    role = db.Column(db.Enum(Roles), default=Roles.MODERATOR)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))

    # Relationships
    user = db.relationship("User", viewonly=True)
    book = db.relationship("Book", viewonly=True)

    def __repr__(self):
        return f"<{self.id}: {self.label}>"
