from flask import redirect, url_for, Blueprint, flash, request
from flask_login import current_user
from sqlalchemy import or_

from app import forms as f, models as m, db
from app.logger import log

bp = Blueprint("permission", __name__, url_prefix="/permission")


@bp.route("/set", methods=["POST"])
def set_permissions():
    form: f.EditPermissionForm = f.EditPermissionForm()

    if form.validate_on_submit():
        book_id = form.book_id.data
        book: m.Book = db.session.get(m.Book, book_id)
        if not book or book.is_deleted or book.owner != current_user:
            log(log.INFO, "User: [%s] is not owner of book: [%s]", current_user, book)
            flash("You are not owner of this book!", "danger")
            return redirect(url_for("book.my_library"))

        user_id = form.user_id.data
        contributor: m.BookContributor = m.BookContributor.query.filter_by(
            user_id=user_id, book_id=book_id
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

        # TODO process data from checkbox tree
        # permissions = json.loads(form.permissions.data)

    return {"status": "ok"}


@bp.route("/access_tree", methods=["GET"])
def access_tree():
    user_id = request.args.get("user_id", type=int)
    book_id = request.args.get("book_id", type=int)
    if not user_id or not book_id:
        return {"message": "get parameters user_id and book_id are required"}, 404

    user: m.User = db.session.get(m.User, user_id)
    if not user:
        return {"message": f"user with id {user_id} not found"}, 404
    book: m.Book = db.session.get(m.Book, book_id)
    if not book:
        return {"message": f"book with id {user_id} not found"}, 404

    access_tree = {
        "book": [],
        "collection": [],
        "section": [],
    }

    users_access_groups: list[m.AccessGroup] = list(
        set(book.list_access_groups).intersection(user.access_groups)
    )

    if list(set(book.access_groups).intersection(users_access_groups)):
        access_tree["book"].append(book_id)

    collections = (
        db.session.query(m.Collection).filter(
            m.Collection.version_id == book.last_version.id,
            m.Collection.is_root == False,  # noqa: E712
            m.Collection.is_deleted == False,  # noqa: E712
        )
    ).all()

    for collection in collections:
        if list(set(collection.access_groups).intersection(users_access_groups)):
            access_tree["collection"].append(collection.id)

    sections = (
        db.session.query(m.Section).filter(
            m.Section.version_id == book.last_version.id,
            m.Section.is_deleted == False,  # noqa: E712
        )
    ).all()

    for section in sections:
        if list(set(section.access_groups).intersection(users_access_groups)):
            access_tree["section"].append(section.id)

    return {"access_tree": access_tree}
