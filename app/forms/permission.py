from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class EditPermissionForm(FlaskForm):
    book_id = IntegerField("Book ID", [DataRequired()])
    user_id = IntegerField("User ID", [DataRequired()])
    permissions = StringField("Permissions JSON", [DataRequired()])
    submit = SubmitField("Edit")
