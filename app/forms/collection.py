from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class BaseCollectionForm(FlaskForm):
    label = StringField("Label", [DataRequired(), Length(3, 256)])
    about = StringField("About")


class CreateCollectionForm(BaseCollectionForm):
    submit = SubmitField("Create")


class EditCollectionForm(BaseCollectionForm):
    submit = SubmitField("Edit")
