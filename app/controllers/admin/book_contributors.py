from flask_admin.base import expose
from flask_admin.helpers import (
    get_redirect_target,
    flash_errors,
)
from flask import redirect, flash, request
from flask_admin.babel import gettext
from wtforms import SelectField
from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_admin.form import form
from flask_admin.model.template import EndpointLinkRowAction

from .protected_model_view import ProtectedModelView
from app import models as m, forms as f
from app.controllers.contributor import (
    add_contributor_to_book,
    delete_contributor_from_book,
)
from app.controllers.permission import set_access_level
from app.logger import log


class BookContributorViewCreateForm(form.Form):
    book = QuerySelectField("Book", get_label="label")
    user = QuerySelectField("User", get_label="username")
    role = SelectField(
        "Role",
        choices=[
            (role.value, role.name)
            for role in m.BookContributor.Roles
            if role.value > 0
        ],
    )


class BookContributorView(ProtectedModelView):
    column_list = ("id", "created_at", "role", "user", "book")
    can_create = True
    can_edit = False
    column_extra_row_actions = [  # Add a new action button
        EndpointLinkRowAction("glyphicon glyphicon-list-alt", ".edit_access_level"),
    ]

    @expose("/edit_access_level/<string:id>", methods=("GET", "POST"))
    def edit_access_level(self, id):
        model: m.BookContributor = self.get_one((id,))

        user = model.user
        book = model.book
        form: f.EditPermissionForm = f.EditPermissionForm()
        if form.validate_on_submit():
            set_access_level(form, book)

        return self.render(
            "admin/contributor_access_level.html", user=user, book=book, id=id
        )

    def create_form(self):
        form = BookContributorViewCreateForm(request.form)
        form.book.query = m.Book.query.filter_by(is_deleted=False)
        form.user.query = m.User.query
        return form

    @expose("/new/", methods=("GET", "POST"))
    def create_view(self):
        return_url = get_redirect_target() or self.get_url(".index_view")

        if not self.can_delete:
            return redirect(return_url)

        form: BookContributorViewCreateForm = self.create_form()

        if (
            form.user.data
            and form.book.data
            and form.book.data.user_id == form.user.data.id
        ):
            flash("This user is owner of this book", "danger")
        elif self.validate_form(form):
            add_contributor_to_book(form, form.book.data.id, user_id=form.user.data.id)

        return self.render("admin/model/create.html", form=form)

    @expose("/delete/", methods=("POST",))
    def delete_view(self):
        return_url = get_redirect_target() or self.get_url(".index_view")

        if not self.can_delete:
            return redirect(return_url)

        form = self.delete_form()

        if self.validate_form(form):
            # id is InputRequired()
            id = form.id.data

            model = self.get_one(id)

            if model is None:
                flash(gettext("Record does not exist."), "error")
                return redirect(return_url)

            try:
                delete_contributor_from_book(form, model.book_id, user_id=model.user_id)
            except Exception as e:
                log(
                    log.EXCEPTION,
                    "AdminPanel delete contributor unexpected error [%s]",
                    str(e),
                )
            return redirect(return_url)

        else:
            flash_errors(form, message="Failed to delete record. %(error)s")

        return redirect(return_url)
