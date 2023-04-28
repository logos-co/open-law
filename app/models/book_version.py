from datetime import datetime

from app import db
from app.models.utils import BaseModel


class BookVersion(BaseModel):
    __tablename__ = "book_versions"

    # need to redeclare id to use it in the derivative relationship
    id = db.Column(db.Integer, primary_key=True)
    semver = db.Column(db.String(16), unique=False, nullable=False)
    exported = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    # Foreign keys
    derivative_id = db.Column(db.Integer, db.ForeignKey("book_versions.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))

    # Relationships
    book = db.relationship("Book", viewonly=True)
    derivative = db.relationship("BookVersion", remote_side=[id])
    sections = db.relationship("Section", viewonly=True)
    collections = db.relationship("Collection", viewonly=True)

    def __repr__(self):
        return f"<{self.id}: {self.semver}>"

    @property
    def root_collection(self):
        for collection in self.collections:
            if collection.is_root:
                return collection

    @property
    def children_collections(self):
        return self.root_collection.children
