from flask import Response
from flask.testing import FlaskClient

from app import models as m, db

from tests.utils import (
    login,
    create_book,
    create_collection,
    create_section,
    create_interpretation,
    create_comment,
    create,
    logout,
)


def test_notifications(client: FlaskClient):
    _, user = login(client)
    user: m.User
    assert user.id

    book = create_book(client)
    collection, _ = create_collection(client, book.id)
    section, _ = create_section(client, book.id, collection.id)
    interpretation, _ = create_interpretation(client, book.id, section.id)
    user_2_id = create(username="user_2")
    user_2: m.User = db.session.get(m.User, user_2_id)
    assert user_2

    response: Response = client.post(
        f"/book/{book.id}/add_contributor",
        data=dict(user_id=user_2.id, role=m.BookContributor.Roles.MODERATOR),
        follow_redirects=True,
    )

    assert response.status_code == 200
    logout(client)
    login(client, user_2.username)
    comment, _ = create_comment(client, book.id, interpretation.id)
    assert comment
    assert comment.user_id == user_2_id
    assert len(user.active_notifications) == 1

    logout(client)
    login(client)
    response: Response = client.post(
        f"/approve/comment/{comment.id}",
        follow_redirects=True,
    )
    assert response.status_code == 200

    response: Response = client.post(
        f"/book/{book.id}/delete_contributor",
        data=dict(user_id=user_2_id),
        follow_redirects=True,
    )
    assert response.status_code == 200

    # check that user_2 have notification about he was added, deleted as Editor/Moderator and his comment was approved
    assert len(user_2.active_notifications) == 3

    response: Response = client.post(
        f"/book/{book.id}/add_contributor",
        data=dict(user_id=user_2.id, role=m.BookContributor.Roles.EDITOR),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert len(user_2.active_notifications) == 4

    logout(client)
    login(client, user_2.username)

    collection_2, _ = create_collection(client, book.id)
    assert collection_2
    assert len(user.active_notifications) == 2

    response: Response = client.post(
        f"/book/{book.id}/{collection_2.id}/edit",
        data=dict(label="Test Collection #1 Label"),
        follow_redirects=True,
    )
    assert response.status_code == 200

    section_2, _ = create_section(client, book.id, collection_2.id)
    interpretation_2, _ = create_interpretation(client, book.id, section_2.id)
    comment_2, _ = create_comment(client, book.id, interpretation_2.id)
    assert interpretation_2
    assert len(user.active_notifications) == 5

    logout(client)
    login(client)
    response: Response = client.post(
        f"/book/{book.id}/{interpretation_2.id}/comment_delete",
        data=dict(
            text=comment.text,
            interpretation_id=interpretation_2.id,
            comment_id=comment_2.id,
        ),
        follow_redirects=True,
    )
    response.status_code == 200

    assert len(user_2.active_notifications) == 5
    response: Response = client.post(
        f"/approve/interpretation/{interpretation_2.id}",
        follow_redirects=True,
    )
    response.status_code == 200
    assert len(user_2.active_notifications) == 6

    response: Response = client.post(
        f"/book/{book.id}/{interpretation_2.id}/delete_interpretation",
        data=dict(interpretation_id=interpretation_2.id),
        follow_redirects=True,
    )
    response.status_code == 200

    assert len(user_2.active_notifications) == 7

    logout(client)
    login(client, user_2.username)
    response: Response = client.post(
        f"/book/{book.id}/{section_2.id}/edit_section",
        data=dict(
            section_id=section_2.id,
            label="Test",
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert len(user.active_notifications) == 6

    response: Response = client.post(
        f"/book/{book.id}/{section_2.id}/delete_section",
        follow_redirects=True,
    )
    assert response.status_code == 200

    response: Response = client.post(
        f"/book/{book.id}/{collection_2.id}/delete",
        follow_redirects=True,
    )
    assert response.status_code == 200

    assert len(user.active_notifications) == 8

    strings = [
        "New interpretation to%",
        "%renamed a section on%",
        "%create a new section on%",
        "%delete a section on%",
        "%create a new collection on%",
        "%renamed a collection on%",
        "%delete a collection on%",
        "New comment to your interpretation",
    ]
    for string in strings:
        notification = m.Notification.query.filter(
            m.Notification.text.ilike(f"{string}")
        ).first()
        assert notification
        assert notification.user_id == user.id

    strings_for_user_2 = [
        "You've been added to%",
        "Your comment has been approved%",
        "You've been removed from%",
        "A moderator has removed your comment",
        "Your interpretation has been approved%",
        "A moderator has removed your interpretation",
    ]
    for string in strings_for_user_2:
        notification = m.Notification.query.filter(
            m.Notification.text.ilike(f"{string}")
        ).first()
        assert notification
        assert notification.user_id == user_2.id

    response: Response = client.get(
        "/notifications/mark_all_as_read",
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert len(user_2.active_notifications) == 0
