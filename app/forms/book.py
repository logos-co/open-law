from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class BaseBookForm(FlaskForm):
    label = StringField("Label", [DataRequired(), Length(4, 256)])
    about = StringField("About")
    tags = StringField("Tags")


class CreateBookForm(BaseBookForm):
    submit = SubmitField("Add new book")


class EditBookForm(BaseBookForm):
    book_id = StringField("User ID", [DataRequired()])
    submit = SubmitField("Edit book")
