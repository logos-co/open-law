from app import models as m
from app.logger import log


def delete_nested_collection_entities(collection: m.Collection):
    collection.is_deleted = True
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
