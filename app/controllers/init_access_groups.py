from app import models as m
from app.logger import log
from .get_or_create_permission import get_or_create_permission


def create_moderator_group():
    log(log.INFO, "Create moderator access group")
    group: m.AccessGroup = m.AccessGroup(name="moderator").save()

    interpretation_DA = get_or_create_permission(
        access=m.Permission.Access.D | m.Permission.Access.A,
        entity_type=m.Permission.Entity.INTERPRETATION,
    )
    comment_DA = get_or_create_permission(
        access=m.Permission.Access.D | m.Permission.Access.A,
        entity_type=m.Permission.Entity.COMMENT,
    )

    log(log.INFO, "Add permission [%d] to group[%d]", interpretation_DA.id, group.id)
    m.PermissionAccessGroups(
        permission_id=interpretation_DA.id, access_group_id=group.id
    ).save()

    log(log.INFO, "Add permission [%d] to group[%d]", comment_DA.id, group.id)
    m.PermissionAccessGroups(
        permission_id=comment_DA.id, access_group_id=group.id
    ).save()

    return group
