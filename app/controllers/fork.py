from flask_login import current_user

from app import models as m
from app.logger import log
from app.controllers.create_access_groups import (
    create_editor_group,
    create_moderator_group,
)


def recursive_copy_collection(
    collection: m.Collection, parent_id: int, version_id: int
):
    collection_copy = m.Collection(
        label=collection.label,
        about=collection.about,
        is_root=collection.is_root,
        is_leaf=collection.is_leaf,
        position=collection.position,
        parent_id=parent_id,
        version_id=version_id,
    )
    log(log.INFO, "Create copy of collection [%s]", collection)
    collection_copy.save()

    if collection.active_sections:
        for section in collection.active_sections:
            section: m.Section
            section_copy = m.Section(
                label=section.label,
                collection_id=collection_copy.id,
                user_id=section.user_id,
                version_id=version_id,
                position=section.position,
            )
            log(log.INFO, "Create copy of section [%s]", section)
            section_copy.save()

            interpretation: m.Interpretation = section.approved_interpretation
            if not interpretation:
                continue

            interpretation_copy = m.Interpretation(
                text=interpretation.text,
                plain_text=interpretation.plain_text,
                approved=interpretation.approved,
                user_id=interpretation.user_id,
                section_id=section_copy.id,
            )
            log(log.INFO, "Create copy of interpretation [%s]", interpretation_copy)
            interpretation_copy.save()

            comments: list[m.Comment] = section.approved_comments
            for comment in comments:
                comment_copy = m.Comment(
                    text=comment.text,
                    approved=comment.approved,
                    edited=comment.edited,
                    user_id=comment.user_id,
                    interpretation_id=interpretation_copy.id,
                )
                log(log.INFO, "Create copy of comment [%s]", comment)
                comment_copy.save()

    elif collection.active_children:
        for child in collection.active_children:
            recursive_copy_collection(child, collection_copy.id, version_id)


def fork_book(book: m.Book, label: str, about: str):
    book_active_version: m.BookVersion = book.active_version
    book_root_collection: m.Collection = book_active_version.root_collection

    book_copy: m.Book = m.Book(
        label=label, about=about, user_id=current_user.id, original_book_id=book.id
    )
    log(log.INFO, "Create fork of book [%s]", book)
    book_copy.save()

    version = m.BookVersion(
        semver="Active", book_id=book_copy.id, is_active=True
    ).save()
    log(log.INFO, "Create new version for book [%s]", book)
    version.save()

    root_collection = m.Collection(
        label="Root Collection", version_id=version.id, is_root=True
    ).save()

    # access groups
    editor_access_group = create_editor_group(book_id=book.id)
    moderator_access_group = create_moderator_group(book_id=book.id)
    access_groups = [editor_access_group, moderator_access_group]

    for access_group in access_groups:
        m.BookAccessGroups(book_id=book.id, access_group_id=access_group.id).save()
        m.CollectionAccessGroups(
            collection_id=root_collection.id, access_group_id=access_group.id
        ).save()
    # -------------

    # tags
    for tag in book.tags:
        m.BookTags(tag_id=tag.id, book_id=book_copy.id).save()
    # ----

    for collection in book_root_collection.active_children:
        recursive_copy_collection(collection, root_collection.id, version.id)

    return version
