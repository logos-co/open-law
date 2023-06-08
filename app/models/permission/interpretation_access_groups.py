from app import db
from app.models.utils import BaseModel


class InterpretationAccessGroups(BaseModel):
    __tablename__ = "interpretations_access_groups"

    # Foreign keys
    interpretation_id = db.Column(db.Integer, db.ForeignKey("interpretations.id"))
    access_group_id = db.Column(db.Integer, db.ForeignKey("access_groups.id"))

    def __repr__(self):
        return f"<c:{self.interpretation_id} to a_g:{self.access_group_id}"
