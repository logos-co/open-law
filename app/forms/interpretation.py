from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class BaseInterpretationForm(FlaskForm):
    about = StringField("About")
    text = StringField("Text")


class CreateInterpretationForm(BaseInterpretationForm):
    label = StringField("Label", [DataRequired(), Length(3, 256)])
    section_id = StringField("Interpretation ID", [DataRequired()])
    submit = SubmitField("Create")


class EditInterpretationForm(BaseInterpretationForm):
    interpretation_id = StringField("Interpretation ID", [DataRequired()])
    submit = SubmitField("Edit")
