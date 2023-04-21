from app import db
from app.models.utils import BaseModel


class InterpretationTag(BaseModel):
    __tablename__ = "interpretation_tags"

    # Foreign keys
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
    interpretation_id = db.Column(db.Integer, db.ForeignKey("interpretations.id"))

    def __repr__(self):
        return f"<t:{self.tag_id} to i:{self.interpretation_id}"
