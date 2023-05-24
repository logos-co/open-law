from app import models as m


def get_or_create_permission(access: int, entity: m.Permission.Entity):
    permission: m.Permission = m.Permission.query.filter_by(
        access=access, entity=entity
    ).first()
    if not permission:
        permission: m.Permission = m.Permission(access=access, entity=entity).save()
    return permission
