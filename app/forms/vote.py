from flask_wtf import FlaskForm
from wtforms import BooleanField


class VoteForm(FlaskForm):
    positive = BooleanField("Positive")
