from flask_login import current_user

from app import models as m
from app.logger import log
from .recursive_copy_functions import recursive_copy_collection


def create_new_version(book: m.Book, semver: str):
    book_active_version: m.BookVersion = book.active_version
    book_root_collection: m.Collection = book_active_version.root_collection

    version: m.BookVersion = m.BookVersion(
        semver=semver,
        derivative_id=book.active_version.id,
        book_id=book.id,
        user_id=current_user.id,
    )
    log(log.INFO, "Create new version for book [%s]", book)
    version.save()

    root_collection = m.Collection(
        label="Root Collection",
        version_id=version.id,
        is_root=True,
        copy_of=book_root_collection.id,
    ).save()

    for collection in book_root_collection.active_children:
        recursive_copy_collection(collection, root_collection.id, version.id)

    return version
