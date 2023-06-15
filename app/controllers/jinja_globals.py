import re

from flask import current_app
from flask_wtf import FlaskForm
from flask import url_for, render_template
from flask_login import current_user
from sqlalchemy import func

from app import models as m

TAG_REGEX = re.compile(r"\[.*?\]")


# Using: {{ form_hidden_tag() }}
def form_hidden_tag():
    form = FlaskForm()
    return form.hidden_tag()


# Using: {{ display_inline_elements("Some text with [tags] here") }}
def display_inline_elements(text: str):
    users_mentions = current_app.config["USER_MENTION_REGEX"].findall(text)
    classes = [
        "!no-underline",
        "cursor-pointer",
        "multiple-input-word",
        "bg-sky-100",
        "border",
        "border-sky-300",
        "dark:!text-black",
        "rounded",
        "text-center",
        "py-1/2",
        "px-1",
    ]
    classes = " ".join(classes)
    for users_mention in users_mentions:
        username = users_mention.replace("@", "").lower()
        user: m.User = m.User.query.filter(
            (func.lower(m.User.username) == username)
        ).first()
        if user:
            username_to_display = users_mention.replace(username, user.username)
            url = url_for("user.profile", user_id=user.id)
            text = text.replace(
                users_mention,
                f"<a href='{url}' class='{classes}'>{username_to_display}</a>",
            )

    tags = current_app.config["TAG_REGEX"].findall(text)
    classes = ["text-orange-500", "!no-underline"]
    classes = " ".join(classes)
    for tag in set(tags):
        url = url_for(
            "search.tag_search_interpretations", tag_name=tag.lower().replace("#", "")
        )
        text = re.sub(
            rf"({tag})\b", f"<a href='{url}' class='{classes}'>{tag}</a>", text
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
        interpretation_id=interpretation.copy_of or interpretation.id,
    )
    return url


# Using: {{ recursive_render("template.html", collection=collection, book=book) }}
def recursive_render(
    template: str, collection: m.Collection, book: m.Book, version: m.BookVersion = None
):
    return render_template(template, collection=collection, book=book, version=version)


# Using: {{ has_permission(entity=book, required_permissions=[Access.create]) }}
def has_permission(
    entity: m.Book | m.Collection | m.Section | m.Interpretation,
    required_permissions: m.Permission.Access | list[m.Permission.Access],
    entity_type: m.Permission.Entity = None,
) -> bool:
    if not current_user.is_authenticated:
        return False

    # check if user is owner of book
    match type(entity):
        case m.Book:
            if entity.user_id == current_user.id:
                return True
        case m.Collection | m.Section:
            if entity.version.book.user_id == current_user.id:
                return True
        case m.Interpretation:
            if entity.book.user_id == current_user.id:
                return True
        case _:
            ...

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
