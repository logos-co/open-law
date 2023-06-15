from app import models as m
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
