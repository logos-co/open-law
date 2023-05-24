from app import db
from app.models.utils import BaseModel


class AccessGroup(BaseModel):
    __tablename__ = "access_groups"

    name = db.Column(db.String(32), unique=True, nullable=False)

    # Relationships
    permissions = db.relationship(
        "Permission",
        secondary="permissions_access_groups",
        back_populates="access_groups",
    )
    users = db.relationship(
        "User", secondary="users_access_groups", back_populates="permissions"
    )
