from flask_login import current_user
from flask import flash, redirect, url_for, request, make_response
import functools

from app import models as m, db
from app.logger import log


def check_permissions(
    entity_type: m.Permission.Entity,
    access: list[m.Permission.Access],
    entities: list[dict],
):
    if not current_user.is_authenticated:
        flash("You do not have permission", "danger")
        return make_response(redirect(url_for("home.get_all")))

    request_args = (
        {**request.view_args, **request.args} if request.view_args else {**request.args}
    )
    entity = None
    for model in entities:
        if not entity:
            entity_id_field = (model.__name__ + "_id").lower()
            entity_id = request_args.get(entity_id_field)
            entity: m.Book | m.Collection | m.Section | m.Interpretation | m.Comment = (
                db.session.get(model, entity_id)
            )

    if entity is None:
        log(log.INFO, "No entity [%s] found", entities)
        flash("You do not have permission", "danger")
        return make_response(redirect(url_for("home.get_all")))

    book_id = request_args.get("book_id")
    if book_id:
        book: m.Book = db.session.get(m.Book, book_id)
        if book and book.user_id == current_user.id:
            # user has access because he is book owner
            log(log.INFO, "User [%s] is book owner [%s]", current_user, book)
            return None

    if type(entity) == m.Comment:
        log(log.INFO, "Entity is Comment. Replace it by entity.interpretation")
        entity = entity.interpretation
    elif (
        type(entity) == m.Interpretation
        and entity.user_id == current_user.id
        and m.Permission.Access.A not in access
    ):
        log(log.INFO, "User [%s] is interpretation creator [%s]", current_user, entity)
        return None

    if not entity or not entity.access_groups:
        log(
            log.INFO,
            "Entity [%s] of entity.access_groups [%s] not found",
            access,
            entity,
        )
        flash("You do not have permission", "warning")
        return make_response(redirect(url_for("home.get_all")))

    # check if user is not owner of book
    if not book_id and entity.access_groups[0].book.user_id == current_user.id:
        # user has access because he is book owner
        log(
            log.INFO,
            "User [%s] is book owner [%s]",
            current_user,
            entity.access_groups[0].book,
        )
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
        log(
            log.INFO,
            "User [%s] has permission to [%s] [%s]",
            access,
            current_user,
            entity,
        )
        return

    log(
        log.INFO,
        "User [%s] dont have permission to [%s] [%s]",
        current_user,
        access,
        entity,
    )
    flash("You do not have permission", "danger")
    return make_response(redirect(url_for("home.get_all")))


def require_permission(
    entity_type: m.Permission.Entity,
    access: list[m.Permission.Access],
    entities: list[dict],
):
    def decorator(f):
        @functools.wraps(f)
        def permission_checker(*args, **kwargs):
            if response := check_permissions(
                entity_type=entity_type,
                access=access,
                entities=entities,
            ):
                return response
            return f(*args, **kwargs)

        return permission_checker

    return decorator
