from datetime import datetime

from sqlalchemy import and_

from app import db, models as m
from app.models.utils import BaseModel


class BookVersion(BaseModel):
    __tablename__ = "book_versions"

    # need to redeclare id to use it in the derivative relationship
    id = db.Column(db.Integer, primary_key=True)
    semver = db.Column(db.String(16), unique=False, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    # Foreign keys
    derivative_id = db.Column(db.Integer, db.ForeignKey("book_versions.id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    user_id = db.Column(db.ForeignKey("users.id"))

    # Relationships
    user = db.relationship("User", viewonly=True)
    book = db.relationship("Book", viewonly=True)
    derivative = db.relationship("BookVersion", remote_side=[id])
    sections = db.relationship("Section", viewonly=True, order_by="desc(Section.id)")
    collections = db.relationship(
        "Collection", viewonly=True, order_by="desc(Collection.id)"
    )

    def __repr__(self):
        return f"<{self.id}: {self.semver}>"

    @property
    def root_collection(self):
        for collection in self.collections:
            if collection.is_root:
                return collection

    @property
    def children_collections(self):
        return [
            collection
            for collection in self.root_collection.children
            if not collection.is_deleted
        ]

    @property
    def approved_comments(self):
        comments = (
            db.session.query(
                m.Comment,
            )
            .filter(
                and_(
                    m.BookVersion.id == self.id,
                    m.Section.version_id == m.BookVersion.id,
                    m.Collection.id == m.Section.collection_id,
                    m.Interpretation.section_id == m.Section.id,
                    m.Comment.interpretation_id == m.Interpretation.id,
                    m.Comment.approved.is_(True),
                    m.Comment.is_deleted.is_(False),
                    m.BookVersion.is_deleted.is_(False),
                    m.Interpretation.is_deleted.is_(False),
                    m.Section.is_deleted.is_(False),
                    m.Collection.is_deleted.is_(False),
                ),
            )
            .order_by(m.Comment.created_at.desc())
            .all()
        )

        return comments

    @property
    def approved_interpretations(self):
        interpretations = (
            db.session.query(
                m.Interpretation,
            )
            .filter(
                and_(
                    m.BookVersion.id == self.id,
                    m.Section.version_id == m.BookVersion.id,
                    m.Collection.id == m.Section.collection_id,
                    m.Interpretation.section_id == m.Section.id,
                    m.Interpretation.approved.is_(True),
                    m.BookVersion.is_deleted.is_(False),
                    m.Interpretation.is_deleted.is_(False),
                    m.Section.is_deleted.is_(False),
                    m.Collection.is_deleted.is_(False),
                ),
            )
            .order_by(m.Interpretation.created_at.desc())
            .all()
        )

        return interpretations

    @property
    def interpretations(self):
        interpretations = (
            db.session.query(
                m.Interpretation,
            )
            .filter(
                and_(
                    m.BookVersion.id == self.id,
                    m.Section.version_id == m.BookVersion.id,
                    m.Collection.id == m.Section.collection_id,
                    m.Interpretation.section_id == m.Section.id,
                    m.BookVersion.is_deleted.is_(False),
                    m.Interpretation.is_deleted.is_(False),
                    m.Section.is_deleted.is_(False),
                    m.Collection.is_deleted.is_(False),
                ),
            )
            .order_by(m.Interpretation.created_at.desc())
            .all()
        )

        return interpretations
