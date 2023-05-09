from flask import current_app as Response
from flask.testing import FlaskClient

from app import models as m
from tests.utils import login


def test_upvote(client: FlaskClient):
    _, user = login(client)

    response: Response = client.post(
        "/vote/interpretation/999",
        data=dict(
            positive=True,
        ),
        follow_redirects=True,
    )

    assert response
    assert response.status_code == 404
    assert response.json["message"] == "Interpretation not found"

    interpretation = m.Interpretation(
        label="Test Interpretation 1 Label",
        text="Test Interpretation 1 Text",
        user_id=user.id,
    ).save()

    assert interpretation.vote_count == 0

    response: Response = client.post(
        f"/vote/interpretation/{interpretation.id}",
        data=dict(
            positive=True,
        ),
        follow_redirects=True,
    )

    assert response
    assert response.status_code == 200
    json = response.json
    assert json
    assert "vote_count" in json
    assert json["vote_count"] == 1
    assert interpretation.vote_count == 1

    response: Response = client.post(
        f"/vote/interpretation/{interpretation.id}",
        data=dict(
            positive=True,
        ),
        follow_redirects=True,
    )

    assert response
    assert response.status_code == 200
    json = response.json
    assert json
    assert "vote_count" in json
    assert json["vote_count"] == 0
    assert interpretation.vote_count == 0

    response: Response = client.post(
        f"/vote/interpretation/{interpretation.id}",
        data=dict(
            positive=False,
        ),
        follow_redirects=True,
    )

    assert response
    assert response.status_code == 200
    json = response.json
    assert json
    assert "vote_count" in json
    assert json["vote_count"] == -1
    assert interpretation.vote_count == -1

    response: Response = client.post(
        f"/vote/interpretation/{interpretation.id}",
        data=dict(
            # positive=False,
        ),
        follow_redirects=True,
    )

    assert response
    assert response.status_code == 200
    json = response.json
    assert json
    assert "vote_count" in json
    assert json["vote_count"] == 0
    assert interpretation.vote_count == 0
