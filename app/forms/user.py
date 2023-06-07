import base64

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    FileField,
    PasswordField,
    SubmitField,
    ValidationError,
    BooleanField,
)
from wtforms.validators import DataRequired, Length, EqualTo
from flask_login import current_user

from app import models as m


class UserForm(FlaskForm):
    next_url = StringField("next_url")
    user_id = StringField("user_id", [DataRequired()])
    activated = BooleanField("activated")
    username = StringField("Username", [DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 30)])
    password_confirmation = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Password do not match."),
        ],
    )
    submit = SubmitField("Save")

    def validate_username(self, field):
        if (
            m.User.query.filter_by(username=field.data)
            .filter(m.User.id != int(self.user_id.data))
            .first()
            is not None
        ):
            raise ValidationError("This username is taken.")
        elif " " in field.data:
            raise ValidationError("User name couldn't have spaces.")


class NewUserForm(FlaskForm):
    activated = BooleanField("activated")
    username = StringField("Username", [DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 30)])
    password_confirmation = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Password do not match."),
        ],
    )
    submit = SubmitField("Save")

    def validate_username(self, field):
        if m.User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError("This username is taken.")


class EditUserForm(FlaskForm):
    username = StringField("Username", [DataRequired()])
    avatar_img = FileField("Avatar file (max 1mb, formats: jpg,jpeg,png)")
    submit = SubmitField("Save")

    def validate_username(self, field):
        if (
            m.User.query.filter_by(username=field.data)
            .filter(m.User.id != current_user.id)
            .first()
        ):
            raise ValidationError("This username is taken.")
        elif " " in field.data:
            raise ValidationError("User name couldn't have spaces.")

    def validate_avatar_img(self, field):
        if field.data:
            img_data = field.data.read()
            img_data = base64.b64encode(img_data)
            img_data = img_data.decode("utf-8")
            field.data = img_data
            size = len(img_data) / 1000000
            if size > 1:
                raise ValidationError("Avatar file size too large")


class ReactivateUserForm(FlaskForm):
    submit = SubmitField("Save")
