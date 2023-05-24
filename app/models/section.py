from sqlalchemy import func, text

from app import db
from app.models.utils import BaseModel
from app.controllers import create_breadcrumbs
from .interpretation import Interpretation
from .comment import Comment
from .interpretation_vote import InterpretationVote


class Section(BaseModel):
    __tablename__ = "sections"

    label = db.Column(db.String(256), unique=False, nullable=False)

    # Foreign keys
    collection_id = db.Column(db.ForeignKey("collections.id"))
    user_id = db.Column(db.ForeignKey("users.id"))
    version_id = db.Column(db.ForeignKey("book_versions.id"))
    selected_interpretation_id = db.Column(db.Integer, nullable=True)

    # Relationships
    collection = db.relationship("Collection", viewonly=True)
    user = db.relationship("User", viewonly=True)
    version = db.relationship("BookVersion", viewonly=True)
    interpretations = db.relationship(
        "Interpretation", viewonly=True, order_by="desc(Interpretation.id)"
    )
    access_groups = db.relationship(
        "AccessGroup",
        secondary="sections_access_groups",
    )  # access_groups related to current entity
    tags = db.relationship(
        "Tag",
        secondary="section_tags",
        back_populates="sections",
    )

    @property
    def path(self):
        parent = self.collection
        grand_parent = parent.parent
        path = f"{self.version.book.label} / "
        if grand_parent.is_root:
            path += f"{parent.label} / "
        else:
            path += f"{grand_parent.label} / {parent.label} / "
        path += self.label
        return path

    @property
    def breadcrumbs_path(self):
        parent = self.collection
        grand_parent = parent.parent
        if grand_parent.is_root:
            collection_path = (parent.id,)
        else:
            collection_path = (
                grand_parent.id,
                parent.id,
            )
        breadcrumbs_path = create_breadcrumbs(self.book_id, collection_path)
        return breadcrumbs_path

    @property
    def book_id(self):
        _book_id = self.version.book_id
        return _book_id

    @property
    def sub_collection_id(self):
        parent = self.collection
        grand_parent = parent.parent
        if grand_parent.is_root:
            _sub_collection_id = parent.id
        else:
            _sub_collection_id = grand_parent.id
        return _sub_collection_id

    @property
    def active_interpretations(self):
        return [
            interpretation
            for interpretation in self.interpretations
            if not interpretation.is_deleted
        ]

    @property
    def approved_interpretation(self):
        interpretation = Interpretation.query.filter_by(
            approved=True, section_id=self.id, is_deleted=False
        ).first()

        if interpretation:
            return interpretation

        # most upvoted
        result = (
            db.session.query(
                Interpretation, func.count(Interpretation.votes).label("total_votes")
            )
            .join(InterpretationVote)
            .filter(
                Interpretation.section_id == self.id, Interpretation.is_deleted is False
            )
            .group_by(Interpretation.id)
            .order_by(text("total_votes DESC"))
        ).first()
        if result:
            return result[0]

        # oldest
        interpretation = (
            Interpretation.query.filter_by(section_id=self.id, is_deleted=False)
            .order_by(Interpretation.created_at)
            .first()
        )

        if interpretation:
            return interpretation

    @property
    def approved_comments(self):
        interpretation_ids = [
            interpretation.id for interpretation in self.interpretations
        ]
        comments = (
            Comment.query.filter_by(approved=True)
            .filter(Comment.interpretation_id.in_(interpretation_ids))
            .all()
        )

        return comments

    def __repr__(self):
        return f"<{self.id}: {self.label}>"
