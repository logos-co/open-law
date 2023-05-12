from flask import current_app as Response
from flask.testing import FlaskClient

from app import models as m
from tests.utils import login


def test_star(client: FlaskClient):
    _, user = login(client)

    response: Response = client.post(
        "/star/999",
        data=dict(
            positive=True,
        ),
        follow_redirects=True,
    )

    assert response
    assert response.status_code == 404
    assert response.json["message"] == "Book not found"

    book = m.Book(
        label="Test Interpretation 1 Label",
        user_id=user.id,
    ).save()

    assert len(book.stars) == 0

    response: Response = client.post(
        f"/star/{book.id}",
        follow_redirects=True,
    )

    assert response
    assert response.status_code == 200
    json = response.json
    assert json
    assert "stars_count" in json
    assert json["stars_count"] == 1
    assert "current_user_star" in json
    assert json["current_user_star"]
    assert len(book.stars) == 1

    response: Response = client.post(
        f"/star/{book.id}",
        follow_redirects=True,
    )

    assert response
    assert response.status_code == 200
    json = response.json
    assert json
    assert "stars_count" in json
    assert json["stars_count"] == 0
    assert "current_user_star" in json
    assert not json["current_user_star"]
    assert len(book.stars) == 0
