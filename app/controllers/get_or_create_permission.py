from app import models as m
from app.logger import log


def get_or_create_permission(access: int, entity_type: m.Permission.Entity):
    permission: m.Permission = m.Permission.query.filter_by(
        access=access, entity_type=entity_type
    ).first()
    if not permission:
        log(log.INFO, "Create permission [%d] for entity [%s]", access, entity_type)
        permission: m.Permission = m.Permission(
            access=access, entity_type=entity_type
        ).save()
    return permission
