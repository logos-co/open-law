from app import db
from app.models.utils import BaseModel


class PermissionAccessGroups(BaseModel):
    __tablename__ = "permissions_access_groups"

    # Foreign keys
    permission_id = db.Column(db.Integer, db.ForeignKey("permissions.id"))
    access_group_id = db.Column(db.Integer, db.ForeignKey("access_groups.id"))

    def __repr__(self):
        return f"<p:{self.permission_id} to a_g:{self.access_group_id}"
