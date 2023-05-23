from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

from app import models as m, db
from app.logger import log


class BaseSectionForm(FlaskForm):
    label = StringField("Label", [DataRequired(), Length(3, 256)])
    about = StringField("About")


class CreateSectionForm(BaseSectionForm):
    collection_id = StringField("Collection ID", [DataRequired()])
    sub_collection_id = StringField("Sub collection ID")
    submit = SubmitField("Create")

    def validate_collection_id(self, field):
        collection_id = field.data
        collection: m.Collection = db.session.get(m.Collection, collection_id)
        if self.sub_collection_id.data and self.sub_collection_id.data != "_":
            collection: m.Collection = db.session.get(
                m.Collection, self.sub_collection_id.data
            )

        if not collection or collection.sub_collections:
            log(log.WARNING, "Collection [%s] it not leaf", collection)

            raise ValidationError("You can't create section for this collection")

    def validate_label(self, field):
        label = field.data
        collection_id = self.collection_id.data

        section: m.Section = m.Section.query.filter_by(
            is_deleted=False, label=label, collection_id=collection_id
        ).first()
        if section:
            log(
                log.WARNING,
                "Section with label [%s] already exists: [%s]",
                label,
                section,
            )
            raise ValidationError("Section label must be unique!")


class EditSectionForm(BaseSectionForm):
    section_id = StringField("Section ID", [DataRequired()])
    submit = SubmitField("Edit")

    def validate_label(self, field):
        label = field.data
        section_id = self.section_id.data

        session = db.session.get(m.Section, section_id)
        if not session:
            log(log.WARNING, "Session with id [%s] not found", section_id)
            raise ValidationError("Invalid session id")

        collection_id = session.collection_id
        section: m.Section = (
            m.Section.query.filter_by(
                is_deleted=False, label=label, collection_id=collection_id
            )
            .filter(m.Section.id != section_id)
            .first()
        )

        if section:
            log(
                log.WARNING,
                "Section with label [%s] already exists: [%s]",
                label,
                section,
            )
            raise ValidationError("Section label must be unique!")
