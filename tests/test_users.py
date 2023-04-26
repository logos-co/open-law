from flask import current_app as app
from flask.testing import FlaskClient, FlaskCliRunner
from click.testing import Result

from app import models as m, db
from tests.utils import login


def test_list(populate: FlaskClient):
    login(populate)
    DEFAULT_PAGE_SIZE = app.config["DEFAULT_PAGE_SIZE"]
    response = populate.get("/user/")
    assert response
    assert response.status_code == 200
    html = response.data.decode()
    users = m.User.query.order_by(m.User.id).limit(11).all()
    assert len(users) == 11
    for user in users[:DEFAULT_PAGE_SIZE]:
        assert user.username in html
    assert users[10].username not in html

    populate.application.config["PAGE_LINKS_NUMBER"] = 6
    response = populate.get("/user/?page=6")
    assert response
    assert response.status_code == 200
    html = response.data.decode()
    assert "/user/?page=6" in html
    assert "/user/?page=3" in html
    assert "/user/?page=8" in html
    assert "/user/?page=10" not in html
    assert "/user/?page=2" not in html


def test_create_admin(runner: FlaskCliRunner):
    res: Result = runner.invoke(args=["create-admin"])
    assert "admin created" in res.output
    assert m.User.query.filter_by(username=app.config["ADMIN_USERNAME"]).first()


def test_delete_user(populate: FlaskClient):
    login(populate)
    users = m.User.query.all()
    uc = len(users)
    response = populate.delete("/user/delete/1")
    assert m.User.query.count() < uc
    assert response.status_code == 200


def test_search_user(populate: FlaskClient, runner: FlaskCliRunner):
    _, current_user = login(populate)
    MAX_SEARCH_RESULTS = populate.application.config["MAX_SEARCH_RESULTS"]

    response = populate.get("/user/search")
    assert response.status_code == 422
    assert response.json["message"] == "q parameter is required"

    q = current_user.username

    response = populate.get(f"/user/search?q={q}")
    assert response.json

    users = response.json.get("users")
    assert users
    assert len(users) <= MAX_SEARCH_RESULTS

    for user in users:
        assert q in user["username"]
        assert user["username"] != current_user

    q = "user"

    response = populate.get(f"/user/search?q={q}")
    assert response.json

    users = response.json.get("users")
    assert users
    assert len(users) <= MAX_SEARCH_RESULTS

    for user in users:
        assert q in user["username"]

    q = "user1"

    response = populate.get(f"/user/search?q={q}")
    assert response.json

    users = response.json.get("users")
    assert users
    assert len(users) <= MAX_SEARCH_RESULTS

    user = users[0]
    assert user["username"] == q

    q = "booboo"

    response = populate.get(f"/user/search?q={q}")
    assert response.json

    users = response.json.get("users")
    assert not users

    # add dummmy data
    runner.invoke(args=["db-populate"])

    response = populate.get("/user/search?q=dummy&book_id=1")
    assert response.json

    book_1 = db.session.get(m.Book, 1)
    contributors_ids = [contributor.user_id for contributor in book_1.contributors]

    users = response.json.get("users")
    assert users
    for user in users:
        user_id = user.get("id")
        assert user_id not in contributors_ids
