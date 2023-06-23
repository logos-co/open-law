from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user, logout_user
from app.controllers import create_pagination
from app.controllers.error_flashes import create_error_flash
from sqlalchemy import func, not_, or_

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
        user.username = form.username.data
        if form.avatar_img.data:
            current_user.avatar_img = (
                form.avatar_img.data
            )  # form.avatar_img.data is changed in form validator
        user.is_activated = True
        user.save()
        return redirect(url_for("main.index"))
    elif form.is_submitted():
        log(log.ERROR, "Update user errors: [%s]", form.errors)
        create_error_flash(form)

    if current_user.is_activated:
        form.username.data = current_user.username
    return render_template("user/edit_profile.html", form=form)


@bp.route("/delete_avatar", methods=["POST"])
@login_required
def delete_avatar():
    user: m.User = current_user
    current_user.avatar_img = None
    log(log.ERROR, "Delete user [%s] avatar", user)
    current_user.save()

    return redirect(url_for("user.edit_profile"))


@bp.route("/<int:user_id>/profile")
def profile(user_id: int):
    user: m.User = db.session.get(m.User, user_id)
    interpretations: m.Interpretation = m.Interpretation.query.filter_by(
        user_id=user_id
    )
    books: m.Interpretation = (
        db.session.query(
            m.Book,
        )
        .join(m.BookContributor, m.BookContributor.book_id == m.Book.id, full=True)
        .filter(
            or_(
                m.Book.user_id == user_id,
                m.BookContributor.user_id == user_id,
            ),
            m.Book.is_deleted == False,  # noqa: E712
        )
    ).all()

    if not user:
        log(log.ERROR, "Not found user by id : [%s]", user_id)
        flash("Cannot find user data", "danger")
    return render_template(
        "user/profile.html", user=user, interpretations=interpretations, books=books
    )


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
    q = request.args.get("q", type=str, default="").lower()
    if not q:
        return jsonify({"message": "q parameter is required"}), 422

    book_id = request.args.get("book_id", type=str, default=None)

    query_user = m.User.query
    query_user = query_user.order_by(m.User.username)

    query_user = query_user.filter(
        or_(
            func.lower(m.User.username).like(f"%{q}%"),
            func.lower(m.User.wallet_id).like(f"%{q}%"),
        )
    )
    if book_id:
        book_contributors = m.BookContributor.query.filter_by(book_id=book_id).all()
        user_ids = [contributor.user_id for contributor in book_contributors]
        user_ids.append(current_user.id)
        query_user = query_user.filter(not_(m.User.id.in_(user_ids)))
    query_user = query_user.limit(configuration.MAX_SEARCH_RESULTS)

    users = [{"username": user.username, "id": user.id} for user in query_user.all()]

    return jsonify({"users": users})
