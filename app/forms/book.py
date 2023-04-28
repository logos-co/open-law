from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CreateBookForm(FlaskForm):
    label = StringField("Label", [DataRequired(), Length(6, 256)])
    submit = SubmitField("Add new book")
