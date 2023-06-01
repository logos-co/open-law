from app import models as m
from app.logger import log
from .get_or_create_permission import get_or_create_permission


def create_moderator_group(book_id: int):
    log(log.INFO, "Create moderator access group")
    group: m.AccessGroup = m.AccessGroup(name="moderator", book_id=book_id).save()
    permissions = []

    comment_DA = get_or_create_permission(
        access=m.Permission.Access.D | m.Permission.Access.A,
        entity_type=m.Permission.Entity.COMMENT,
    )
    permissions.append(comment_DA)

    interpretation_DA = get_or_create_permission(
        access=m.Permission.Access.D | m.Permission.Access.A,
        entity_type=m.Permission.Entity.INTERPRETATION,
    )
    permissions.append(interpretation_DA)

    for permission in permissions:
        log(log.INFO, "Add permission [%d] to group[%d]", permission.id, group.id)
        m.PermissionAccessGroups(
            permission_id=permission.id, access_group_id=group.id
        ).save()

    return group


def create_editor_group(book_id: int):
    log(log.INFO, "Create editor access group")
    group: m.AccessGroup = m.AccessGroup(name="editor", book_id=book_id).save()
    permissions = []

    comment_DA = get_or_create_permission(
        access=m.Permission.Access.D | m.Permission.Access.A,
        entity_type=m.Permission.Entity.COMMENT,
    )
    permissions.append(comment_DA)

    interpretation_DA = get_or_create_permission(
        access=m.Permission.Access.D | m.Permission.Access.A,
        entity_type=m.Permission.Entity.INTERPRETATION,
    )
    permissions.append(interpretation_DA)

    section_CUD = get_or_create_permission(
        access=m.Permission.Access.C | m.Permission.Access.U | m.Permission.Access.D,
        entity_type=m.Permission.Entity.SECTION,
    )
    permissions.append(section_CUD)

    collection_CUD = get_or_create_permission(
        access=m.Permission.Access.C | m.Permission.Access.U | m.Permission.Access.D,
        entity_type=m.Permission.Entity.COLLECTION,
    )
    permissions.append(collection_CUD)

    book_U = get_or_create_permission(
        access=m.Permission.Access.U,
        entity_type=m.Permission.Entity.BOOK,
    )
    permissions.append(book_U)

    for permission in permissions:
        log(log.INFO, "Add permission [%d] to group[%d]", permission.id, group.id)
        m.PermissionAccessGroups(
            permission_id=permission.id, access_group_id=group.id
        ).save()

    return group
