from flask import (
    Blueprint,
)

from app.controllers import (
    book_validator,
)


bp = Blueprint("book", __name__, url_prefix="/book")


@bp.before_request
def before_request():
    if response := book_validator():
        return response
