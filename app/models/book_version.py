from datetime import datetime

from app import db
from app.models.utils import BaseModel


class BookVersion(BaseModel):
    __tablename__ = "book_versions"

    # need to redeclare id to use it in the derivative relationship
    id = db.Column(db.Integer, primary_key=True)
    semver = db.Column(db.String(1024), unique=False, nullable=False)
    exported = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    # Foreign keys
    derivative_id = db.Column(db.Integer, db.ForeignKey("book_versions.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))

    # Relationships
    book = db.relationship("Book", viewonly=True)
    derivative = db.relationship("BookVersion", remote_side=[id])

    def __repr__(self):
        return f"<{self.id}: {self.semver}>"
