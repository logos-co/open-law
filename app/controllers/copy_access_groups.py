from app import models as m, db
from app.logger import log


def copy_access_groups(
    copy_from: m.Book or m.Collection or m.Interpretation or m.Section, copy_to
):
    for access_group in copy_from.access_groups:
        log(
            log.INFO,
            "Copy access group %s from %s to %s",
            access_group,
            copy_from,
            copy_to,
        )

        match type(copy_to):
            case m.Book:
                m.BookAccessGroups(
                    book_id=copy_to.id, access_group_id=access_group.id
                ).save()
            case m.Collection:
                m.CollectionAccessGroups(
                    collection_id=copy_to.id, access_group_id=access_group.id
                ).save()
            case m.Interpretation:
                m.InterpretationAccessGroups(
                    interpretation_id=copy_to.id, access_group_id=access_group.id
                ).save()
            case m.Section:
                m.SectionAccessGroups(
                    section_id=copy_to.id, access_group_id=access_group.id
                ).save()


def recursive_copy_access_groups(
    copy_from: m.Book or m.Collection or m.Interpretation or m.Section, copy_to
):
    current_access_groups = None

    match type(copy_to):
        case m.Book:
            current_access_groups = m.BookAccessGroups.query.filter_by(
                book_id=copy_to.id
            ).all()
        case m.Collection:
            current_access_groups = m.CollectionAccessGroups.query.filter_by(
                collection_id=copy_to.id
            ).all()
        case m.Interpretation:
            current_access_groups = m.InterpretationAccessGroups.query.filter_by(
                interpretation_id=copy_to.id
            ).all()
        case m.Section:
            current_access_groups = m.SectionAccessGroups.query.filter_by(
                section_id=copy_to.id
            ).all()

    if current_access_groups:
        for access_group in current_access_groups:
            db.session.delete(access_group)
        db.session.commit()

    copy_access_groups(copy_from, copy_to)

    if hasattr(copy_to, "active_children"):
        for collection in copy_to.active_children:
            recursive_copy_access_groups(copy_to, collection)

    if hasattr(copy_to, "active_sections"):
        for section in copy_to.active_sections:
            recursive_copy_access_groups(copy_to, section)

    if hasattr(copy_to, "active_interpretations"):
        for interpretations in copy_to.active_interpretations:
            recursive_copy_access_groups(copy_to, interpretations)
