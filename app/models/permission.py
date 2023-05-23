from enum import IntEnum

from app import db
from app.models.utils import BaseModel

# access groups
#   moderators(by default empty) -> root collection -> CRUD Interpretation, Comment
#   editors(by default empty) -> root collection -> CRUD Collection, Section
#
#   on create collection/section -> inherit parent's access groups
#

# add to collection, sections, ...
#  - access_groups -> access group table

# access group:
#   - name
#   - users many-to-many = []
#   - permissions many-to-many = []

# permission:
#   - access [Enum(CRUD)]
#   - entity [Enum(collection, sections, ...)]
#   - access_group -> access group table

C = 1
R = 2
U = 4
D = 8


class _Permission(BaseModel):
    __tablename__ = "permissions"

    # PAY ATTENTION ON SUB COLLECTIONS

    class Access(IntEnum):
        UNKNOWN = 0
        C = 1
        R = 2
        CR = 3
        U = 4
        CU = 5
        RU = 6
        CRU = 7
        D = 8

    access_to_entity = db.Column(db.Enum(AccessTo), default=AccessTo.UNKNOWN)
    access_to_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # Relationships
    user = db.relationship("User", viewonly=True)

    def __repr__(self):
        return f"<{self.id}: u:{self.user_id} b:{self.book_id}>"


class Permission(BaseModel):
    __tablename__ = "permissions"

    # PAY ATTENTION ON SUB COLLECTIONS

    class AccessTo(IntEnum):
        UNKNOWN = 0
        BOOK = 1
        COLLECTION = 2
        SUB_COLLECTION = 3
        SECTION = 4

    access_to_entity = db.Column(db.Enum(AccessTo), default=AccessTo.UNKNOWN)
    access_to_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # Relationships
    user = db.relationship("User", viewonly=True)

    def __repr__(self):
        return f"<{self.id}: u:{self.user_id} b:{self.book_id}>"
