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
    position = db.Column(db.Integer, default=-1, nullable=True)

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
    access_groups = db.relationship(
        "AccessGroup",
        secondary="collections_access_groups",
    )  # access_groups related to current entity

    def __repr__(self):
        return f"<{self.id}: {self.label}>"

    @property
    def active_sections(self):
        items = [section for section in self.sections if not section.is_deleted]
        items.sort(key=lambda item: item.position)
        return items

    @property
    def active_children(self):
        items = [child for child in self.children if not child.is_deleted]
        items.sort(key=lambda item: item.position)
        return items

    @property
    def book_id(self):
        return self.version.book_id

    @property
    def sub_collections(self):
        return [
            sub_collection
            for sub_collection in self.children
            if not sub_collection.is_deleted
        ]
