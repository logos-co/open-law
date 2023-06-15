from enum import IntEnum

from app.models.utils import BaseModel
from app import db


class Notification(BaseModel):
    __tablename__ = "notifications"

    class Actions(IntEnum):
        CREATE = 1
        EDIT = 2
        DELETE = 3
        VOTE = 4
        APPROVE = 5
        CONTRIBUTING = 6
        MENTION = 7

    class Entities(IntEnum):
        SECTION = 1
        COLLECTION = 2
        INTERPRETATION = 3
        COMMENT = 4
        BOOK = 5

    action = db.Column(db.Enum(Actions))
    entity = db.Column(db.Enum(Entities))
    entity_id = db.Column(db.Integer, nullable=False)

    link = db.Column(db.String(256), unique=False, nullable=False)
    text = db.Column(db.String(256), unique=False, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    # Foreign keys
    user_id = db.Column(db.ForeignKey("users.id"))  # for what user notification is

    # Relationships
    user = db.relationship("User", viewonly=True)  # for what user notification is
