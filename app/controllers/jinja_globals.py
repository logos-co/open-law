import re

from flask import current_app
from flask_wtf import FlaskForm
from flask import url_for, render_template

from app import models as m

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
        url = url_for(
            "search.tag_search_interpretations",
            tag_name=tag.lower().replace("[", "").replace("]", ""),
        )
        text = text.replace(
            tag,
            f"<a href='{url}' class='{classes}'>{tag}</a>",
        )

    return text


# Using: {{ build_qa_url(interpretation) }}
def build_qa_url_using_interpretation(interpretation: m.Interpretation):
    section: m.Section = interpretation.section
    collection: m.Collection = section.collection
    if collection.parent and not collection.parent.is_root:
        collection: m.Collection = collection.parent
    book: m.Book = section.version.book

    url = url_for(
        "book.qa_view",
        book_id=book.id,
        interpretation_id=interpretation.id,
    )
    return url


def recursive_render(collection: m.Collection, book: m.Book):
    return render_template(
        "book/components/sub_collection_tab_content.html",
        collection=collection,
        book=book,
    )
