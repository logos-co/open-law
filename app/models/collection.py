from app import db
from app.models.utils import BaseModel


class Collection(BaseModel):
    __tablename__ = "collections"

    # need to redeclare id to use it in the parent relationship
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(256), unique=False, nullable=False)
    about = db.Column(db.Text, unique=False, nullable=True)
    is_root = db.Column(db.Boolean, default=False)
    is_leaf = db.Column(db.Boolean, default=False)

    # Foreign keys
    version_id = db.Column(db.ForeignKey("book_versions.id"))
    parent_id = db.Column(db.ForeignKey("collections.id"))

    # Relationships
    version = db.relationship("BookVersion")
    children = db.relationship(
        "Collection",
        backref=db.backref("parent", remote_side=[id]),
        viewonly=True,
        order_by="asc(Collection.id)",
    )
    sections = db.relationship("Section")

    def __repr__(self):
        return f"<{self.id}: {self.label}>"

    @property
    def active_sections(self):
        return [section for section in self.sections if not section.is_deleted]

    @property
    def sub_collections(self):
        return [
            sub_collection
            for sub_collection in self.children
            if not sub_collection.is_deleted
        ]
