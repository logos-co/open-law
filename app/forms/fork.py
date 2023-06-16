from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ForkBookForm(FlaskForm):
    label = StringField("Fork Label", [DataRequired()])
    about = StringField("Fork About")


class ForkVersionForm(FlaskForm):
    version_id = StringField("Version ID", [DataRequired()])
    label = StringField("Fork Label", [DataRequired()])
    about = StringField("Fork About")
