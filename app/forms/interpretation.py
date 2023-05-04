from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length

from app import models as m, db
from app.logger import log


class BaseInterpretationForm(FlaskForm):
    label = StringField("Label", [DataRequired(), Length(3, 256)])
    about = StringField("About")


class CreateInterpretationForm(BaseInterpretationForm):
    section_id = StringField("Interpretation ID", [DataRequired()])
    text = StringField("Text")
    submit = SubmitField("Create")

    def validate_label(self, field):
        label = field.data
        section_id = self.section_id.data

        interpretation: m.Interpretation = m.Interpretation.query.filter_by(
            is_deleted=False, label=label, section_id=section_id
        ).first()
        if interpretation:
            log(
                log.WARNING,
                "Interpretation with label [%s] already exists: [%s]",
                label,
                interpretation,
            )
            raise ValidationError("Interpretation label must be unique!")


class EditInterpretationForm(BaseInterpretationForm):
    interpretation_id = StringField("Interpretation ID", [DataRequired()])
    text = StringField("Text")
    submit = SubmitField("Edit")

    def validate_label(self, field):
        label = field.data
        interpretation_id = self.interpretation_id.data

        section_id = db.session.get(m.Interpretation, interpretation_id).section_id

        interpretation: m.Interpretation = (
            m.Interpretation.query.filter_by(
                is_deleted=False, label=label, section_id=section_id
            )
            .filter(m.Interpretation.id != interpretation_id)
            .first()
        )

        if interpretation:
            log(
                log.WARNING,
                "Interpretation with label [%s] already exists: [%s]",
                label,
                interpretation,
            )
            raise ValidationError("Interpretation label must be unique!")
