from flask import redirect, url_for, Blueprint


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    return redirect(url_for("home.get_all"))
