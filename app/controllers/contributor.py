from flask import flash, redirect, url_for

from app import forms as f, models as m, db
from app.logger import log


def add_contributor_to_book(
    form: f.AddContributorForm,
    book_id: int,
    selected_tab: str = "",
    user_id: int = None,
):
    if not user_id:
        user_id = form.user_id.data
    book_contributor = m.BookContributor.query.filter_by(
        user_id=user_id, book_id=book_id
    ).first()
    if book_contributor:
        log(log.INFO, "Contributor: [%s] already exists", book_contributor)
        flash("Already exists!", "danger")
        return redirect(
            url_for("book.settings", selected_tab=selected_tab, book_id=book_id)
        )

    role = m.BookContributor.Roles(int(form.role.data))
    contributor = m.BookContributor(user_id=user_id, book_id=book_id, role=role)
    log(log.INFO, "New contributor [%s]", contributor)
    contributor.save()

    groups = (
        db.session.query(m.AccessGroup)
        .filter(
            m.BookAccessGroups.book_id == book_id,
            m.AccessGroup.id == m.BookAccessGroups.access_group_id,
            m.AccessGroup.name == role.name.lower(),
        )
        .all()
    )
    for group in groups:
        m.UserAccessGroups(user_id=user_id, access_group_id=group.id).save()

    flash("Contributor was added!", "success")
    return redirect(
        url_for("book.settings", selected_tab=selected_tab, book_id=book_id)
    )


def delete_contributor_from_book(
    form: f.DeleteContributorForm,
    book_id: int,
    selected_tab: str = "",
    user_id: int = None,
):
    if not user_id:
        user_id = form.user_id.data
    book_contributor = m.BookContributor.query.filter_by(
        user_id=user_id, book_id=book_id
    ).first()
    if not book_contributor:
        log(
            log.INFO,
            "BookContributor does not exists user: [%s], book: [%s]",
            user_id,
            book_id,
        )
        flash("Does not exists!", "success")
        return redirect(
            url_for("book.settings", selected_tab=selected_tab, book_id=book_id)
        )

    book: m.Book = db.session.get(m.Book, book_id)
    user: m.User = db.session.get(m.User, user_id)
    if book:
        for access_group in book.access_groups:
            access_group: m.AccessGroup
            if user in access_group.users:
                log(
                    log.INFO,
                    "Delete user [%s] from AccessGroup [%s]",
                    user,
                    access_group,
                )
                relationships_to_delete = m.UserAccessGroups.query.filter_by(
                    user_id=user_id, access_group_id=access_group.id
                ).all()
                for relationship in relationships_to_delete:
                    db.session.delete(relationship)

    log(log.INFO, "Delete BookContributor [%s]", book_contributor)
    db.session.delete(book_contributor)
    db.session.commit()

    flash("Success!", "success")
    return redirect(
        url_for("book.settings", selected_tab=selected_tab, book_id=book_id)
    )
