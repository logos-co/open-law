from flask import Blueprint, render_template, url_for, redirect, flash, request, session
from flask_login import login_user, logout_user, login_required

from app import models as m
from app import forms as f
from app.logger import log


auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = f.LoginForm(request.form)
    if form.validate_on_submit():
        user = m.User.authenticate(form.user_id.data, form.password.data)
        log(log.INFO, "Form submitted. User: [%s]", user)
        if user:
            login_user(user)
            log(log.INFO, "Login successful.")
            flash("Login successful.", "success")
            return redirect(url_for("main.index"))
        flash("Wrong user ID or password.", "danger")

    elif form.is_submitted():
        log(log.WARNING, "Form submitted error: [%s]", form.errors)
    return render_template("auth/login.html", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    log(log.INFO, "You were logged out.")
    session.clear()
    return redirect(url_for("auth.login"))
