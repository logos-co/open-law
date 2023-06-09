import json

from flask_login import current_user
from flask import flash, redirect, url_for

from app.logger import log
from app import models as m, db, forms as f
from app.controllers.create_access_groups import (
    create_editor_group,
    create_moderator_group,
)


def set_access_level(form: f.EditPermissionForm, book: m.Book):
    user_id = form.user_id.data
    contributor: m.BookContributor = m.BookContributor.query.filter_by(
        user_id=user_id, book_id=book.id
    ).first()
    if not contributor:
        log(
            log.INFO,
            "User: [%s] is not contributor of book: [%s]",
            current_user,
            book,
        )
        flash("User are not contributor of this book!", "danger")
        return redirect(url_for("book.my_library"))

    user: m.User = contributor.user
    users_access_groups: list[m.AccessGroup] = list(
        set(book.list_access_groups).intersection(user.access_groups)
    )
    if len(users_access_groups) > 1:
        log(
            log.WARNING,
            "User: [%s] has more than 1 access group in book [%s]",
            user,
            book,
        )

    for users_access in users_access_groups:
        users_access: m.AccessGroup
        users_access.users.remove(user)

    permissions_json = json.loads(form.permissions.data)
    book_ids = permissions_json.get("book", [])
    for book_id in book_ids:
        entire_boot_access_group = m.AccessGroup.query.filter_by(
            book_id=book_id, name=contributor.role.name.lower()
        ).first()
        m.UserAccessGroups(
            user_id=user.id, access_group_id=entire_boot_access_group.id
        ).save(False)
        db.session.commit()
        flash("Success!", "success")
        return redirect(url_for("book.settings", book_id=book.id))

    new_access_group = None
    match contributor.role:
        case m.BookContributor.Roles.EDITOR:
            new_access_group = create_editor_group(book.id)
        case m.BookContributor.Roles.MODERATOR:
            new_access_group = create_moderator_group(book.id)
        case _:
            log(
                log.CRITICAL,
                "Unknown contributor's [%s] role: [%s]",
                contributor,
                contributor.role,
            )
            flash("Unknown contributor's role", "danger")
            return redirect(url_for("book.settings", book_id=book.id))
    m.UserAccessGroups(user_id=user.id, access_group_id=new_access_group.id).save(False)

    collection_ids = permissions_json.get("collection", [])
    for collection_id in collection_ids:
        m.CollectionAccessGroups(
            collection_id=collection_id, access_group_id=new_access_group.id
        ).save(False)

    section_ids = permissions_json.get("section", [])
    for section_id in section_ids:
        m.SectionAccessGroups(
            section_id=section_id, access_group_id=new_access_group.id
        ).save(False)

    db.session.commit()
    flash("Success!", "success")
    return redirect(url_for("book.settings", book_id=book.id))
