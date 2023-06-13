from app import models as m
from app.logger import log


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
        copy_of=collection.id,
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
                copy_of=section.id,
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
                copy_of=interpretation.id,
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
                    copy_of=comment.id,
                )
                log(log.INFO, "Create copy of comment [%s]", comment)
                comment_copy.save()

    elif collection.active_children:
        for child in collection.active_children:
            recursive_copy_collection(child, collection_copy.id, version_id)


def create_new_version(book: m.Book, semver: str):
    book_active_version: m.BookVersion = book.active_version
    book_root_collection: m.Collection = book_active_version.root_collection

    version: m.BookVersion = m.BookVersion(
        semver=semver, derivative_id=book.active_version.id, book_id=book.id
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
