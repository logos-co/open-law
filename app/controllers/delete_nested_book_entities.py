from app import models as m
from app.logger import log


def delete_nested_book_entities(book: m.Book):
    for version in book.versions:
        version: m.BookVersion
        version.is_deleted = True
        log(log.INFO, "Delete version [%s]", version.id)
        version.save(False)

        delete_nested_version_entities(version)


def delete_nested_version_entities(book_version: m.BookVersion):
    root_collection: m.Collection = book_version.root_collection
    root_collection.is_deleted = True
    log(log.INFO, "Delete root collection [%s]", root_collection.id)
    root_collection.save(False)

    for collection in root_collection.children:
        collection: m.Collection
        collection.is_deleted = True
        log(log.INFO, "Delete collection [%s]", collection.id)
        collection.save(False)

        delete_nested_collection_entities(collection)


def delete_nested_collection_entities(collection: m.Collection):
    for section in collection.sections:
        section: m.Section
        section.is_deleted = True
        log(log.INFO, "Delete section [%s]", section.id)
        section.save(False)

        delete_nested_section_entities(section)


def delete_nested_section_entities(section: m.Section):
    for interpretation in section.interpretations:
        interpretation: m.Interpretation
        interpretation.is_deleted = True
        log(log.INFO, "Delete interpretation [%s]", interpretation.id)
        interpretation.save(False)

        delete_nested_interpretation_entities(interpretation)


def delete_nested_interpretation_entities(interpretation: m.Interpretation):
    for comment in interpretation.comments:
        comment: m.Comment
        comment.is_deleted = True
        log(log.INFO, "Delete comment [%s]", comment.id)
        comment.save(False)

        delete_nested_comment_entities(comment)


def delete_nested_comment_entities(comment: m.Comment):
    for child in comment.children:
        child: m.Comment
        child.is_deleted = True
        log(log.INFO, "Delete sub comment [%s]", comment.id)
        child.save(False)
