from flask_login import current_user

from app import models as m
from app.logger import log
from app.controllers.create_access_groups import (
    create_editor_group,
    create_moderator_group,
)
from .recursive_copy_functions import recursive_copy_collection, copy_book_version


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
    editor_access_group = create_editor_group(book_id=book_copy.id)
    moderator_access_group = create_moderator_group(book_id=book_copy.id)
    access_groups = [editor_access_group, moderator_access_group]

    for access_group in access_groups:
        m.BookAccessGroups(book_id=book_copy.id, access_group_id=access_group.id).save()
        m.CollectionAccessGroups(
            collection_id=root_collection.id, access_group_id=access_group.id
        ).save()
    # -------------

    # tags
    for tag in book.tags:
        m.BookTags(tag_id=tag.id, book_id=book_copy.id).save()
    # ----

    for collection in book_root_collection.active_children:
        recursive_copy_collection(
            collection, root_collection.id, version.id, False, book=book_copy
        )
    for version in book.actual_versions:
        copy_book_version(book_copy, version)

    return version
