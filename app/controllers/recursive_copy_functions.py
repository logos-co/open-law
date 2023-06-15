from app import models as m
from app.logger import log
from .copy_access_groups import copy_access_groups


def recursive_copy_collection(
    collection: m.Collection,
    parent_id: int,
    version_id: int,
    add_copy_of: bool = True,
    book: m.Book = None,
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
    if add_copy_of:
        collection_copy.copy_of = collection.id
    log(log.INFO, "Create copy of collection [%s]", collection)
    collection_copy.save()

    if book:
        copy_access_groups(book, collection_copy)

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
            if add_copy_of:
                section_copy.copy_of = section.id
            log(log.INFO, "Create copy of section [%s]", section)
            section_copy.save()
            copy_access_groups(collection_copy, section_copy)

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
            if add_copy_of:
                interpretation_copy.copy_of = interpretation.id
            log(log.INFO, "Create copy of interpretation [%s]", interpretation_copy)
            interpretation_copy.save()
            copy_access_groups(section_copy, interpretation_copy)

            comments: list[m.Comment] = section.approved_comments
            for comment in comments:
                comment_copy = m.Comment(
                    text=comment.text,
                    approved=comment.approved,
                    edited=comment.edited,
                    user_id=comment.user_id,
                    interpretation_id=interpretation_copy.id,
                )
                if add_copy_of:
                    comment_copy.copy_of = comment.id
                log(log.INFO, "Create copy of comment [%s]", comment)
                comment_copy.save()

    elif collection.active_children:
        for child in collection.active_children:
            recursive_copy_collection(
                child, collection_copy.id, version_id, add_copy_of, book=book
            )


def copy_book_version(book: m.Book, version: m.BookVersion):
    version_copy: m.BookVersion = m.BookVersion(
        semver=version.semver,
        is_active=version.is_active,
        created_at=version.created_at,
        updated_at=version.updated_at,
        derivative_id=book.active_version.id,
        book_id=book.id,
        user_id=version.user_id,
    )
    log(log.INFO, "Create copy of version [%s]", version)
    version_copy.save()

    root_collection = m.Collection(
        label="Root Collection",
        version_id=version_copy.id,
        is_root=True,
        copy_of=book.active_version.root_collection.id,
    ).save()

    for collection in book.active_version.root_collection.active_children:
        recursive_copy_collection(collection, root_collection.id, version.id, book=book)
