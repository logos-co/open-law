from app import db
from app.models.utils import BaseModel


class UserAccessGroups(BaseModel):
    __tablename__ = "users_access_groups"

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    access_group_id = db.Column(db.Integer, db.ForeignKey("access_groups.id"))

    def __repr__(self):
        return f"<u:{self.user_id} to a_g:{self.access_group_id}"
