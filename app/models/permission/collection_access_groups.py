from app import db
from app.models.utils import BaseModel


class CollectionAccessGroups(BaseModel):
    __tablename__ = "collections_access_groups"

    # Foreign keys
    collection_id = db.Column(db.Integer, db.ForeignKey("collections.id"))
    access_group_id = db.Column(db.Integer, db.ForeignKey("access_groups.id"))

    def __repr__(self):
        return f"<c:{self.collection_id} to a_g:{self.access_group_id}"
