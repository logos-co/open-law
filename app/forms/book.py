from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class BaseBookForm(FlaskForm):
    label = StringField("Label", [DataRequired(), Length(6, 256)])


class CreateBookForm(BaseBookForm):
    submit = SubmitField("Add new book")


class EditBookForm(BaseBookForm):
    submit = SubmitField("Edit book")
