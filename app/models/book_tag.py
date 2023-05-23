from app import db
from app.models.utils import BaseModel


class BookTags(BaseModel):
    __tablename__ = "book_tags"

    # Foreign keys
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))

    def __repr__(self):
        return f"<t:{self.tag_id} to b:{self.book_id}"
