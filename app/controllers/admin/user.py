from .protected_model_view import ProtectedModelView


class UsersView(ProtectedModelView):
    column_list = (
        "id",
        "username",
        "is_activated",
        "wallet_id",
        "is_super_user",
    )
