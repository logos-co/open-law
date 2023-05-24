from app import db
from app.models.utils import BaseModel


class BookAccessGroups(BaseModel):
    __tablename__ = "books_access_groups"

    # Foreign keys
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    access_group_id = db.Column(db.Integer, db.ForeignKey("access_groups.id"))

    def __repr__(self):
        return f"<b:{self.book_id} to a_g:{self.access_group_id}"
