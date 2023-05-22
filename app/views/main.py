from flask import redirect, url_for, Blueprint, render_template

from app import forms as f, models as m


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def index():
    return redirect(url_for("home.get_all"))


@main_blueprint.route("/search", methods=["POST"])
def search():
    form = f.SearchForm()
    if form.validate_on_submit():
        q = form.search_query.data
        users = m.User.query.order_by(m.User.id)
        if q:
            users = users.filter(m.User.username.like(f"%{q}%"))
        interpretations = m.Interpretation.query.order_by(m.Interpretation.id)
        if q:
            interpretations = interpretations.filter(
                m.Interpretation.text.like(f"%{q}%")
            )
        tags = m.Tag.query.order_by(m.Tag.id)
        if q:
            tags = tags.filter(m.Tag.name.like(f"%{q}%"))
        books = m.Book.query.order_by(m.Book.id)
        if q:
            books = books.filter(m.Book.label.like(f"%{q}%"))
    return render_template(
        "searchResult.html",
        query=q,
        users=users,
        interpretations=interpretations,
        tags=tags,
        books=books,
    )
