import re

from flask import current_app
from flask_wtf import FlaskForm

TAG_REGEX = re.compile(r"\[.*?\]")


# Using: {{ form_hidden_tag() }}
def form_hidden_tag():
    form = FlaskForm()
    return form.hidden_tag()


# Using: {{ display_tags("Some text with [tags] here") }}
def display_tags(text: str):
    tags = current_app.config["TAG_REGEX"].findall(text)

    classes = ["text-orange-500", "!no-underline"]
    classes = " ".join(classes)

    for tag in tags:
        text = text.replace(
            tag,
            f"<a href='#' target='_blank' class='{classes}'>{tag}</a>",
        )

    return text
