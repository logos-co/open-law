from flask_admin.base import expose
from flask_admin.helpers import get_redirect_target, flash_errors
from flask import redirect, flash
from flask_admin.babel import gettext

from app.controllers.delete_nested_book_entities import (
    delete_nested_comment_entities,
)
from .protected_model_view import ProtectedModelView


class TagView(ProtectedModelView):
    column_list = (
        "id",
        "name",
        "created_at",
    )

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

            model.is_deleted = True
            delete_nested_comment_entities(model)
            model.save()
            flash(
                gettext(
                    "Section and nested entities were successfully deleted.",
                ),
                "success",
            )
            return redirect(return_url)
        else:
            flash_errors(form, message="Failed to delete record. %(error)s")

        return redirect(return_url)
