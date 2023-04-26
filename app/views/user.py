from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.controllers import create_pagination
from sqlalchemy import not_

from app import models as m, db
from app import forms as f
from app.logger import log
from config import config

configuration = config()
bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/", methods=["GET"])
@login_required
def get_all():
    q = request.args.get("q", type=str, default=None)
    users = m.User.query.order_by(m.User.id)
    if q:
        users = users.filter(m.User.username.like(f"{q}%"))

    pagination = create_pagination(total=users.count())

    return render_template(
        "user/users.html",
        users=users.paginate(page=pagination.page, per_page=pagination.per_page),
        page=pagination,
        search_query=q,
    )


@bp.route("/save", methods=["POST"])
@login_required
def save():
    form = f.UserForm()
    if form.validate_on_submit():
        u: m.User = m.User.query.get(int(form.user_id.data))
        if not u:
            log(log.ERROR, "Not found user by id : [%s]", form.user_id.data)
            flash("Cannot save user data", "danger")
        u.username = form.username.data
        u.activated = form.activated.data
        if form.password.data.strip("*\n "):
            u.password = form.password.data
        u.save()
        if form.next_url.data:
            return redirect(form.next_url.data)
        return redirect(url_for("user.get_all"))

    else:
        log(log.ERROR, "User save errors: [%s]", form.errors)
        flash(f"{form.errors}", "danger")
        return redirect(url_for("user.get_all"))


@bp.route("/create", methods=["POST"])
@login_required
def create():
    form = f.NewUserForm()
    if form.validate_on_submit():
        user = m.User(
            username=form.username.data,
            password=form.password.data,
            activated=form.activated.data,
        )
        log(log.INFO, "Form submitted. User: [%s]", user)
        flash("User added!", "success")
        user.save()
        return redirect(url_for("user.get_all"))


@bp.route("/delete/<id>", methods=["DELETE"])
@login_required
def delete(id):
    u = m.User.query.filter_by(id=id).first()
    if not u:
        log(log.INFO, "There is no user with id: [%s]", id)
        flash("There is no such user", "danger")
        return "no user", 404

    db.session.delete(u)
    db.session.commit()
    log(log.INFO, "User deleted. User: [%s]", u)
    flash("User deleted!", "success")
    return "ok", 200


@bp.route("/search", methods=["GET"])
@login_required
def search():
    q = request.args.get("q", type=str, default=None)
    if not q:
        return jsonify({"message": "q parameter is required"}), 422

    book_id = request.args.get("book_id", type=str, default=None)

    query_user = m.User.query
    query_user = query_user.order_by(m.User.username)

    query_user = query_user.filter(m.User.username.ilike(f"{q}%"))
    if book_id:
        book_contributors = m.BookContributor.query.filter_by(book_id=book_id).all()
        user_ids = [contributor.user_id for contributor in book_contributors]
        user_ids.append(current_user.id)
        query_user = query_user.filter(not_(m.User.id.in_(user_ids)))
    query_user = query_user.limit(configuration.MAX_SEARCH_RESULTS)

    users = [{"username": user.username, "id": user.id} for user in query_user.all()]

    return jsonify({"users": users})
