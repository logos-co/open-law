from flask import current_app as Response
from flask.testing import FlaskClient

from app import models as m
from tests.utils import (
    login,
    logout,
    create_book,
    create_collection,
    create_section,
    create_interpretation,
    create_comment,
)


def test_approve_interpretation(client: FlaskClient):
    dummy_user = m.User(username="test", password="test").save()
    login(client, "test", "test")
    book = create_book(client)
    collection, _ = create_collection(client, book.id)
    section, _ = create_section(client, book.id, collection.id)
    interpretation, _ = create_interpretation(client, book.id, section.id)

    logout(client)
    login(client)

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

    logout(client)
    login(client, "test", "test")

    interpretation: m.Interpretation = m.Interpretation.query.filter_by(
        user_id=dummy_user.id
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
        user_id=dummy_user.id
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
    dummy_user = m.User(username="test", password="test").save()
    login(client, "test", "test")
    book = create_book(client)
    collection, _ = create_collection(client, book.id)
    section, _ = create_section(client, book.id, collection.id)
    interpretation, _ = create_interpretation(client, book.id, section.id)
    comment, _ = create_comment(client, book.id, interpretation.id)

    logout(client)
    login(client)

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

    logout(client)
    login(client, "test", "test")

    comment: m.Comment = m.Comment.query.filter_by(user_id=dummy_user.id).first()
    response: Response = client.post(
        f"/approve/comment/{comment.id}",
        follow_redirects=True,
    )

    assert response
    assert response.json["message"] == "success"
    assert response.json["approve"]
    assert comment.approved

    comment: m.Collection = m.Comment.query.filter_by(user_id=dummy_user.id).first()
    response: Response = client.post(
        f"/approve/comment/{comment.id}",
        follow_redirects=True,
    )

    assert response
    assert response.json["message"] == "success"
    assert not response.json["approve"]
    assert not comment.approved
