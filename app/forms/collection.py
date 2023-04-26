from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CreateCollectionForm(FlaskForm):
    label = StringField("Label", [DataRequired(), Length(6, 1024)])
    about = StringField("About")

    submit = SubmitField("Create")


class EditCollectionForm(FlaskForm):
    label = StringField("Label", [Length(6, 1024)])
    about = StringField("About")

    submit = SubmitField("Edit")
