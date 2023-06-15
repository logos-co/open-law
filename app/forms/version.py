from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, ValidationError
from wtforms.validators import DataRequired

from app import models as m, db


class BaseVersionForm(FlaskForm):
    version_id = IntegerField("Version ID")

    def validate_version_id(self, field):
        version: m.BookVersion = db.session.get(m.BookVersion, field.data)
        if not version:
            raise ValidationError("Version not found")


class EditVersionForm(BaseVersionForm):
    semver = StringField("Semver")
    submit = SubmitField("Edit")

    def validate_semver(self, field):
        version: m.BookVersion = db.session.get(m.BookVersion, self.version_id.data)
        if not version:
            raise ValidationError("Version not found")
        version_semvers = [version.semver.lower() for version in version.book.versions]
        if field.data.lower() in version_semvers:
            raise ValidationError("Version name must me unique")


class DeleteVersionForm(BaseVersionForm):
    submit = SubmitField("Delete")


class CreateVersionForm(FlaskForm):
    semver = StringField("Semver", validators=[DataRequired()])
    submit = SubmitField("Delete")
