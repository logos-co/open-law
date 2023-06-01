from flask import current_app as Response
from flask.testing import FlaskClient

from app import models as m
from tests.utils import login, create_test_book


def test_approve_interpretation(client: FlaskClient):
    _, user = login(client)
    create_test_book(user.id)

    dummy_user = m.User(username="Bob").save()
    create_test_book(dummy_user.id)

    response: Response = client.post(
        "/approve/interpretation/999",
        data=dict(
            positive=True,
        ),
        follow_redirects=True,
    )

    assert response
    assert b"You do not have permission" in response.data

    interpretation: m.Interpretation = m.Interpretation.query.filter_by(
        user_id=dummy_user.id
    ).first()
    response: Response = client.post(
        f"/approve/interpretation/{interpretation.id}",
        follow_redirects=True,
    )

    assert response
    assert b"You do not have permission" in response.data

    interpretation: m.Interpretation = m.Interpretation.query.filter_by(
        user_id=user.id
    ).first()
    response: Response = client.post(
        f"/approve/interpretation/{interpretation.id}",
        follow_redirects=True,
    )

    assert response
    assert response.json["message"] == "success"
    assert response.json["approve"]
    assert interpretation.approved

    interpretation: m.Interpretation = m.Interpretation.query.filter_by(
        user_id=user.id
    ).first()
    response: Response = client.post(
        f"/approve/interpretation/{interpretation.id}",
        follow_redirects=True,
    )

    assert response
    assert response.json["message"] == "success"
    assert not response.json["approve"]
    assert not interpretation.approved


def test_approve_comment(client: FlaskClient):
    _, user = login(client)
    create_test_book(user.id)

    dummy_user = m.User(username="Bob").save()
    create_test_book(dummy_user.id)

    response: Response = client.post(
        "/approve/comment/999",
        data=dict(
            positive=True,
        ),
        follow_redirects=True,
    )

    assert response
    assert b"You do not have permission" in response.data

    comment: m.Comment = m.Comment.query.filter_by(user_id=dummy_user.id).first()
    response: Response = client.post(
        f"/approve/comment/{comment.id}",
        follow_redirects=True,
    )

    assert response
    assert b"You do not have permission" in response.data

    comment: m.Comment = m.Comment.query.filter_by(user_id=user.id).first()
    response: Response = client.post(
        f"/approve/comment/{comment.id}",
        follow_redirects=True,
    )

    assert response
    assert response.json["message"] == "success"
    assert response.json["approve"]
    assert comment.approved

    comment: m.Collection = m.Comment.query.filter_by(user_id=user.id).first()
    response: Response = client.post(
        f"/approve/comment/{comment.id}",
        follow_redirects=True,
    )

    assert response
    assert response.json["message"] == "success"
    assert not response.json["approve"]
    assert not comment.approved
