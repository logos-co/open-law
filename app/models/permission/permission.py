from enum import IntEnum

from app import db
from app.models.utils import BaseModel


class Permission(BaseModel):
    __tablename__ = "permissions"

    class Access(IntEnum):
        C = 1  # 0b0001
        R = 2  # 0b0010
        U = 4  # 0b0100
        D = 8  # 0b1000
        # sum = 0b1111

    class Entity(IntEnum):
        UNKNOWN = 0
        BOOK = 1
        COLLECTION = 2
        SECTION = 3
        INTERPRETATION = 4
        COMMENT = 5

    access = db.Column(db.Integer(), default=Access.C | Access.R | Access.U | Access.D)
    entity = db.Column(db.Enum(Entity), default=Entity.UNKNOWN)

    # Relationships
    access_groups = db.relationship(
        "AccessGroup",
        secondary="permissions_access_groups",
        back_populates="permissions",
    )
