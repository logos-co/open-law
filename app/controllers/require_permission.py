from flask_login import current_user
from flask import flash, redirect, url_for, request, make_response
import functools

from app import models as m, db
from app.logger import log


def check_permissions(
    entity_type: m.Permission.Entity,
    access: list[m.Permission.Access],
    model: m,
    entity_id_field: str,
):
    request_args = (
        {**request.view_args, **request.args} if request.view_args else {**request.args}
    )

    entity_id = request_args.get(entity_id_field)
    if entity_id is None:
        raise ValueError("entity_id not found")
    entity: m.Book | m.Collection | m.Section | m.Interpretation = db.session.get(
        model, entity_id
    )
    if not entity or not entity.access_groups:
        flash("You do not have permission", "warning")
        return make_response(redirect(url_for("home.get_all")))

    # check if user is not owner of book
    if entity.access_groups[0].book.user_id == current_user.id:
        return None

    access_group_query = (
        m.AccessGroup.query.join(
            m.PermissionAccessGroups,
            m.PermissionAccessGroups.access_group_id == m.AccessGroup.id,
        )
        .join(m.Permission, m.PermissionAccessGroups.permission_id == m.Permission.id)
        .filter(
            m.AccessGroup.id.in_(
                [access_group.id for access_group in entity.access_groups]
            )
        )
        .filter(m.AccessGroup.users.any(id=current_user.id))
        .filter(m.Permission.entity_type == entity_type)
    )

    for access in access:
        access_group_query = access_group_query.filter(
            m.Permission.access.op("&")(access) > 0
        )

    access_groups = access_group_query.all()

    if access_groups:
        return

    flash("You do not have permission", "danger")
    return make_response(redirect(url_for("home.get_all")))


def require_permission(
    entity_type: m.Permission.Entity,
    access: list[m.Permission.Access],
    model: m,
    entity_id_field: str,
):
    def decorator(f):
        @functools.wraps(f)
        def permission_checker(*args, **kwargs):
            if response := check_permissions(
                entity_type=entity_type,
                access=access,
                model=model,
                entity_id_field=entity_id_field,
            ):
                return response
            return f(*args, **kwargs)

        return permission_checker

    return decorator
