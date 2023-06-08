from flask_admin import AdminIndexView
from flask_login import current_user
from flask import redirect, url_for


class CustomAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_super_user

    def is_visible(self):
        # This view won't appear in the menu structure
        return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("main.index"))
