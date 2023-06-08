from app.models.utils import BaseModel
from app import db


class Notification(BaseModel):
    __tablename__ = "notifications"
    link = db.Column(db.String(256), unique=False, nullable=False)
    text = db.Column(db.String(256), unique=False, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    # Foreign keys
    user_id = db.Column(db.ForeignKey("users.id"))  # for what user notification is

    # Relationships
    user = db.relationship("User", viewonly=True)  # for what user notification is
