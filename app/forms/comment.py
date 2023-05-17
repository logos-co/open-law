from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class BaseCommentForm(FlaskForm):
    text = StringField("Text", [DataRequired(), Length(3, 256)])
    tags = StringField("Tags")


class CreateCommentForm(BaseCommentForm):
    parent_id = StringField("Text")
    submit = SubmitField("Create")


class DeleteCommentForm(FlaskForm):
    comment_id = StringField("Text")
    submit = SubmitField("Delete")


class EditCommentForm(BaseCommentForm):
    comment_id = StringField("Text")
    submit = SubmitField("Edit")
