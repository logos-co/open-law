from app import db
from app.models.utils import BaseModel


class AccessGroup(BaseModel):
    __tablename__ = "access_groups"

    name = db.Column(db.String(32), nullable=False)

    # Foreign Keys
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))

    # Relationships
    book = db.relationship("Book", viewonly=True)
    permissions = db.relationship(
        "Permission",
        secondary="permissions_access_groups",
        back_populates="access_groups",
    )
    users = db.relationship(
        "User", secondary="users_access_groups", back_populates="access_groups"
    )

    def __repr__(self):
        return f"<{self.id}: {self.name} | Book: {self.book_id}>"
