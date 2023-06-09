from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class ProtectedModelView(ModelView):
    action_disallowed_list = ["delete"]
    column_default_sort = "id"
    can_create = False

    def is_accessible(self):
        return current_user.is_super_user
