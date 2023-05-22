from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class BaseInterpretationForm(FlaskForm):
    about = StringField("About")
    text = StringField("Text")


class CreateInterpretationForm(BaseInterpretationForm):
    section_id = StringField("Interpretation ID", [DataRequired()])
    submit = SubmitField("Create")


class EditInterpretationForm(BaseInterpretationForm):
    interpretation_id = StringField("Interpretation ID", [DataRequired()])
    submit = SubmitField("Edit")
