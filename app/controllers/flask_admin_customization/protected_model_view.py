from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for


class ProtectedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_super_user

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("main.index"))
