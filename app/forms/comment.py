from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class BaseCommentForm(FlaskForm):
    text = StringField("Text", [DataRequired(), Length(3, 256)])
    marked = BooleanField("Marked")
    included_with_interpretation = BooleanField("Included")


class CreateCommentForm(BaseCommentForm):
    submit = SubmitField("Create")
