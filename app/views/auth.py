# flake8: noqa F501
import re
from http import HTTPStatus as status
from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    flash,
    request,
    session,
    jsonify,
    current_app,
)

from flask_login import login_user, logout_user, login_required

from app import models as m
from app import forms as f
from app.logger import log

from siwe.siwe import (
    SiweMessage,
    generate_nonce,
    ValidationError,
    ExpiredMessage,
    MalformedSession,
    InvalidSignature,
)
from web3 import HTTPProvider

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
    return redirect(url_for("main.index"))


@auth_blueprint.route("/nonce")
def nonce():
    session["nonce"] = generate_nonce()
    return session["nonce"]


PATTERN_FORMAT_JS = re.compile(r"(?<!^)(?=[A-Z])")


@auth_blueprint.route("/verify", methods=["POST"])
def verify():
    body = request.get_json()
    if body["message"] is None:
        return (
            jsonify("Expected prepareMessage object as body."),
            400,
        )

    siwe_message = SiweMessage(
        message={
            PATTERN_FORMAT_JS.sub("_", k).lower(): v for k, v in body["message"].items()
        }
    )

    try:
        siwe_message.verify(
            body["signature"],
            provider=HTTPProvider(current_app.config["HTTP_PROVIDER_URL"]),
        )

        if siwe_message.nonce != session["nonce"]:
            return jsonify("invalid nonce"), 400

        session["siwe"] = siwe_message.dict()
        user = m.User.query.filter_by(wallet_id=siwe_message.address).first()
        if not user:
            # Create user
            user: m.User = m.User(
                wallet_id=siwe_message.address,
            ).save()
            login_user(user=user)
            log(log.INFO, "Register new user")
            flash("User created and logged in successful.", "success")
            return redirect(url_for("user.profile"))
        login_user(user=user)
        log(log.INFO, "Verify success.")
        flash("Verify success.", "success")
        return redirect(url_for("home.get_all"))

    except ValidationError:
        session.pop("siwe", default=None)
        session.pop("nonce", default=None)
        print("Authentication attempt rejected due to invalid message.")
        return None
    except ExpiredMessage:
        session.pop("siwe", default=None)
        session.pop("nonce", default=None)
        print("Authentication attempt rejected due to expired message.")
        return None
    except MalformedSession as e:
        session.pop("siwe", default=None)
        session.pop("nonce", default=None)
        print(
            f"Authentication attempt rejected due to missing fields: {', '.join(e.missing_fields)}"
        )
        return None
    except InvalidSignature:
        session.pop("siwe", default=None)
        session.pop("nonce", default=None)
        print("Authentication attempt rejected due to invalid signature.")
        return None
