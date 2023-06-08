from flask import current_app as Response
from flask.testing import FlaskClient

from app import models as m
from tests.utils import (
    login,
    create_interpretation,
    create_section,
    create_book,
    create_collection,
)


def test_upvote_interpretation(client: FlaskClient):
    _, user = login(client)

    response: Response = client.post(
        "/vote/interpretation/999",
        headers={"Content-Type": "application/json"},
        json=dict(
            positive=True,
        ),
        follow_redirects=True,
    )

    assert response
    assert response.status_code == 404
    assert response.json["message"] == "Interpretation not found"

    book = create_book(client)
    assert book
    collection, _ = create_collection(client=client, book_id=book.id)
    assert collection
    section, _ = create_section(
        client=client, book_id=book.id, collection_id=collection.id
    )
    assert section
    interpretation, _ = create_interpretation(
        client=client, book_id=book.id, section_id=section.id
    )

    assert interpretation.vote_count == 0

    response: Response = client.post(
        f"/vote/interpretation/{interpretation.id}",
        headers={"Content-Type": "application/json"},
        json=dict(
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
    assert "current_user_vote" in json
    assert json["current_user_vote"]
    assert interpretation.vote_count == 1

    response: Response = client.post(
        f"/vote/interpretation/{interpretation.id}",
        headers={"Content-Type": "application/json"},
        json=dict(
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
    assert "current_user_vote" in json
    assert json["current_user_vote"] is None
    assert interpretation.vote_count == 0

    response: Response = client.post(
        f"/vote/interpretation/{interpretation.id}",
        headers={"Content-Type": "application/json"},
        json=dict(
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
    assert "current_user_vote" in json
    assert not json["current_user_vote"]
    assert interpretation.vote_count == -1

    response: Response = client.post(
        f"/vote/interpretation/{interpretation.id}",
        headers={"Content-Type": "application/json"},
        json=dict(
            positive=False,
        ),
        follow_redirects=True,
    )

    assert response
    assert response.status_code == 200
    json = response.json
    assert json
    assert "vote_count" in json
    assert json["vote_count"] == 0
    assert "current_user_vote" in json
    assert json["current_user_vote"] is None
    assert interpretation.vote_count == 0


def test_upvote_comment(client: FlaskClient):
    _, user = login(client)

    response: Response = client.post(
        "/vote/comment/999",
        headers={"Content-Type": "application/json"},
        json=dict(
            positive=True,
        ),
        follow_redirects=True,
    )

    assert response
    assert response.status_code == 404
    assert response.json["message"] == "Comment not found"

    comment = m.Comment(
        text="Test Comment 1 Text",
        user_id=user.id,
    ).save()

    assert comment.vote_count == 0

    response: Response = client.post(
        f"/vote/comment/{comment.id}",
        headers={"Content-Type": "application/json"},
        json=dict(
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
    assert "current_user_vote" in json
    assert json["current_user_vote"]
    assert comment.vote_count == 1

    response: Response = client.post(
        f"/vote/comment/{comment.id}",
        headers={"Content-Type": "application/json"},
        json=dict(
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
    assert "current_user_vote" in json
    assert json["current_user_vote"] is None
    assert comment.vote_count == 0

    response: Response = client.post(
        f"/vote/comment/{comment.id}",
        headers={"Content-Type": "application/json"},
        json=dict(
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
    assert "current_user_vote" in json
    assert not json["current_user_vote"]
    assert comment.vote_count == -1

    response: Response = client.post(
        f"/vote/comment/{comment.id}",
        headers={"Content-Type": "application/json"},
        json=dict(
            positive=False,
        ),
        follow_redirects=True,
    )

    assert response
    assert response.status_code == 200
    json = response.json
    assert json
    assert "vote_count" in json
    assert json["vote_count"] == 0
    assert "current_user_vote" in json
    assert json["current_user_vote"] is None
    assert comment.vote_count == 0
