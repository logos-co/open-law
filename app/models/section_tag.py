from app import db
from app.models.utils import BaseModel


class SectionTag(BaseModel):
    __tablename__ = "section_tags"

    # Foreign keys
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
    section_id = db.Column(db.Integer, db.ForeignKey("sections.id"))

    def __repr__(self):
        return f"<t:{self.tag_id} to i:{self.section_id}"
