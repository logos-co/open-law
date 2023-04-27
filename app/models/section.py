from app import db
from app.models.utils import BaseModel


class Section(BaseModel):
    __tablename__ = "sections"

    label = db.Column(db.String(1024), unique=False, nullable=False)
    about = db.Column(db.Text, unique=False, nullable=True)

    # Foreign keys
    collection_id = db.Column(db.ForeignKey("collections.id"))
    user_id = db.Column(db.ForeignKey("users.id"))
    version_id = db.Column(db.ForeignKey("book_versions.id"))
    selected_interpretation_id = db.Column(db.Integer, nullable=True)

    # Relationships
    collection = db.relationship("Collection", viewonly=True)
    user = db.relationship("User", viewonly=True)
    version = db.relationship("BookVersion", viewonly=True)
    interpretations = db.relationship("Interpretation", viewonly=True)

    @property
    def path(self):
        parent = self.collection
        grand_parent = parent.parent
        path = f"{self.version.book.label} / "
        if grand_parent.is_root:
            path += f"{parent.label} / "
        else:
            path += f"{grand_parent.label} / {parent.label} / "
        path += self.label
        return path

    def __repr__(self):
        return f"<{self.id}: {self.label}>"
