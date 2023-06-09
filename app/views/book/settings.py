from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
)
from flask_login import login_required

from app.controllers import (
    register_book_verify_route,
)
from app import models as m, db, forms as f
from app.controllers.require_permission import require_permission
from app.controllers.contributor import (
    add_contributor_to_book,
    delete_contributor_from_book,
)
from app.logger import log
from .bp import bp


@bp.route("/<int:book_id>/settings", methods=["GET"])
@register_book_verify_route(bp.name)
@require_permission(
    entity_type=m.Permission.Entity.BOOK,
    access=[m.Permission.Access.U],
    entities=[m.Book],
)
@login_required
def settings(book_id: int):
    book: m.Book = db.session.get(m.Book, book_id)
    selected_tab = request.args.get("selected_tab", "book_settings")

    return render_template(
        "book/settings.html",
        book=book,
        selected_tab=selected_tab,
        roles=m.BookContributor.Roles,
    )


@bp.route("/<int:book_id>/add_contributor", methods=["POST"])
@register_book_verify_route(bp.name)
@require_permission(
    entity_type=m.Permission.Entity.BOOK,
    access=[m.Permission.Access.U],
    entities=[m.Book],
)
@login_required
def add_contributor(book_id: int):
    form = f.AddContributorForm()
    selected_tab = "user_permissions"
    if form.validate_on_submit():
        response = add_contributor_to_book(form, book_id, selected_tab)
        return response
    else:
        log(log.ERROR, "Book create errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(
            url_for("book.settings", selected_tab=selected_tab, book_id=book_id)
        )


@bp.route("/<int:book_id>/delete_contributor", methods=["POST"])
@register_book_verify_route(bp.name)
@require_permission(
    entity_type=m.Permission.Entity.BOOK,
    access=[m.Permission.Access.U],
    entities=[m.Book],
)
@login_required
def delete_contributor(book_id: int):
    form = f.DeleteContributorForm()
    selected_tab = "user_permissions"

    if form.validate_on_submit():
        response = delete_contributor_from_book(form, book_id, selected_tab)
        return response
    else:
        log(log.ERROR, "Delete contributor errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(
            url_for("book.settings", selected_tab=selected_tab, book_id=book_id)
        )


@bp.route("/<int:book_id>/edit_contributor_role", methods=["POST"])
@register_book_verify_route(bp.name)
@require_permission(
    entity_type=m.Permission.Entity.BOOK,
    access=[m.Permission.Access.U],
    entities=[m.Book],
)
@login_required
def edit_contributor_role(book_id: int):
    form = f.EditContributorRoleForm()
    selected_tab = "user_permissions"

    if form.validate_on_submit():
        book_contributor: m.BookContributor = m.BookContributor.query.filter_by(
            user_id=int(form.user_id.data), book_id=book_id
        ).first()
        if not book_contributor:
            log(
                log.INFO,
                "BookContributor does not exists user: [%s], book: [%s]",
                form.user_id.data,
                book_id,
            )
            flash("Does not exists!", "success")
            return redirect(
                url_for("book.settings", selected_tab=selected_tab, book_id=book_id)
            )

        role = m.BookContributor.Roles(int(form.role.data))

        # change access group
        current_group = m.AccessGroup.query.filter_by(
            book_id=book_id, name=book_contributor.role.name.lower()
        ).first()
        user_access_group = m.UserAccessGroups.query.filter_by(
            user_id=book_contributor.user_id, access_group_id=current_group.id
        ).first()
        if user_access_group:
            db.session.delete(user_access_group)

        new_group = m.AccessGroup.query.filter_by(
            book_id=book_id, name=role.name.lower()
        ).first()
        m.UserAccessGroups(
            user_id=book_contributor.user_id, access_group_id=new_group.id
        ).save(False)

        book_contributor.role = role

        log(
            log.INFO,
            "Update contributor [%s] role: new role: [%s]",
            book_contributor,
            role,
        )
        book_contributor.save()

        flash("Success!", "success")
        return redirect(
            url_for("book.settings", selected_tab=selected_tab, book_id=book_id)
        )
    else:
        log(log.ERROR, "Edit contributor errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")
        return redirect(
            url_for("book.settings", selected_tab=selected_tab, book_id=book_id)
        )
