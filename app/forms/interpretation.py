from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired

from app.controllers import clean_html
from app.logger import log


class BaseInterpretationForm(FlaskForm):
    about = StringField("About")
    text = StringField("Text")


class CreateInterpretationForm(BaseInterpretationForm):
    section_id = StringField("Interpretation ID", [DataRequired()])
    submit = SubmitField("Create")

    def validate_text(self, field):
        text = clean_html(field.data)
        text = text.replace("&nbsp;", "")
        text = text.strip()
        if len(text) < 1:
            log(log.WARNING, "Can't submit empty interpretation")
            raise ValidationError("You can't create interpretation with no text")


class EditInterpretationForm(BaseInterpretationForm):
    interpretation_id = StringField("Interpretation ID", [DataRequired()])
    submit = SubmitField("Edit")
