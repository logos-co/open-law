from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class BaseInterpretationForm(FlaskForm):
    label = StringField("Label", [DataRequired(), Length(3, 256)])
    about = StringField("About")


class CreateInterpretationForm(BaseInterpretationForm):
    section_id = StringField("Interpretation ID", [DataRequired()])
    text = StringField("Text")
    submit = SubmitField("Create")


class EditInterpretationForm(BaseInterpretationForm):
    interpretation_id = StringField("Interpretation ID", [DataRequired()])
    text = StringField("Text")
    submit = SubmitField("Edit")
