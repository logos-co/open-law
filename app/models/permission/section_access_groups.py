from app import db
from app.models.utils import BaseModel


class SectionAccessGroups(BaseModel):
    __tablename__ = "sections_access_groups"

    # Foreign keys
    section_id = db.Column(db.Integer, db.ForeignKey("sections.id"))
    access_group_id = db.Column(db.Integer, db.ForeignKey("access_groups.id"))

    def __repr__(self):
        return f"<s:{self.section_id} to a_g:{self.access_group_id}"
