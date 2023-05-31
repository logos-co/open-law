import re

from flask import current_app
from flask_wtf import FlaskForm
from flask import url_for, render_template
from flask_login import current_user

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


# Using: {{ recursive_render("template.html", collection=collection, book=book) }}
def recursive_render(template: str, collection: m.Collection, book: m.Book):
    return render_template(
        template,
        collection=collection,
        book=book,
    )


# Using: {{ has_permission(entity=book, required_permissions=[Access.create]) }}
def has_permission(
    entity: m.Book | m.Collection | m.Section | m.Interpretation,
    required_permissions: m.Permission.Access | list[m.Permission.Access],
    entity_type: m.Permission.Entity = None,
) -> bool:
    if not current_user.is_authenticated:
        return False

    if type(required_permissions) == m.Permission.Access:
        required_permissions = [required_permissions]

    access_groups: list[m.AccessGroup] = list(
        set(entity.access_groups).intersection(current_user.access_groups)
    )

    if not access_groups:
        return False

    if not entity_type:
        entity_type = m.Permission.Entity[type(entity).__name__.upper()]

    for access_group in access_groups:
        for permission in access_group.permissions:
            permission: m.Permission
            if permission.entity_type != entity_type:
                continue
            for required_permission in required_permissions:
                if permission.access & required_permission:
                    return True

    return False
