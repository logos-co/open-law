from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, flash
from app.logger import log


class ProtectedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_super_user

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("main.index"))

    def delete_model(self, model):
        """
        Delete model.
        :param model:
            Model to delete
        """
        try:
            self.on_model_delete(model)
            # Add your custom logic here and don't forget to commit any changes e.g.
            # self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash("Failed to delete record.", "danger")
                log(log.WARNING, "Failed to delete record.Because [%s]", ex)

            self.session.rollback()

            return False
        else:
            self.after_model_delete(model)

        return True
