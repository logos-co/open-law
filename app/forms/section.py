from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from flask import request

from app import models as m, db
from app.logger import log


class BaseSectionForm(FlaskForm):
    label = StringField("Label", [DataRequired(), Length(3, 256)])
    about = StringField("About")


class CreateSectionForm(BaseSectionForm):
    submit = SubmitField("Create")

    def validate_label(self, field):
        request_args = (
            {**request.view_args, **request.args}
            if request.view_args
            else {**request.args}
        )
        collection_id = request_args["collection_id"]
        collection: m.Collection = db.session.get(m.Collection, collection_id)

        if not collection or collection.sub_collections:
            log(log.WARNING, "Collection [%s] it not leaf", collection)

            raise ValidationError("You can't create section for this collection")

        label = field.data

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
