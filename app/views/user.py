import base64

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user, logout_user
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


@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = f.EditUserForm()
    if form.validate_on_submit():
        user: m.User = current_user
        user.username = form.name.data
        if form.avatar_img.data:
            img_data = form.avatar_img.data.read()
            img_data = base64.b64encode(img_data)
            current_user.avatar_img = img_data.decode("utf-8")
        user.is_activated = True
        user.save()
        return redirect(url_for("main.index"))
    elif form.is_submitted():
        log(log.ERROR, "Update user errors: [%s]", form.errors)
        for field, errors in form.errors.items():
            field_label = form._fields[field].label.text
            for error in errors:
                flash(error.replace("Field", field_label), "danger")

    if current_user.is_activated:
        form.name.data = current_user.username
    return render_template("user/edit_profile.html", form=form)


@bp.route("/<int:user_id>/profile")
def profile(user_id: int):
    user: m.User = m.User.query.get(user_id)
    interpretations: m.Interpretation = m.Interpretation.query.filter_by(
        user_id=user_id
    )
    if not user:
        log(log.ERROR, "Not found user by id : [%s]", user_id)
        flash("Cannot find user data", "danger")
    return render_template(
        "user/profile.html", user=user, interpretations=interpretations
    )


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


@bp.route("/profile_delete", methods=["POST"])
@login_required
def profile_delete():
    user: m.User = db.session.get(m.User, current_user.id)
    user.is_deleted = True
    log(log.INFO, "User deleted. User: [%s]", user)
    user.save()
    logout_user()
    flash("User deleted!", "success")
    return redirect(url_for("home.get_all"))


@bp.route("/profile_reactivate", methods=["GET", "POST"])
def profile_reactivate():
    user: m.User = db.session.get(m.User, current_user.id)
    if not user:
        log(log.CRITICAL, "No such user. User: [%s]", user)
        return redirect(url_for("home.get_all"))
    form = f.ReactivateUserForm()
    if form.validate_on_submit():
        user.is_deleted = False
        log(log.INFO, "Form submitted. User reactivated: [%s]", user)
        flash("User reactivated!", "success")
        user.save()
        return redirect(url_for("home.get_all"))
    return render_template("user/reactivate.html", form=form)


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
