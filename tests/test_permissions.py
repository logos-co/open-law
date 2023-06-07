import json

from flask import current_app as Response

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


def test_editor_access_to_entire_book(client):
    login(client)
    book = create_book(client)

    editor = m.User(username="editor", password="editor").save()
    response: Response = client.post(
        f"/book/{book.id}/add_contributor",
        data=dict(user_id=editor.id, role=m.BookContributor.Roles.EDITOR),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Contributor was added!" in response.data
    logout(client)

    login(client, "editor", "editor")

    # access to settings page
    response: Response = client.get(f"/book/{book.id}/settings", follow_redirects=True)
    assert b"You do not have permission" not in response.data

    # access to edit book
    response: Response = client.post(
        f"/book/{book.id}/edit",
        data=dict(book_id=book.id, label="BookEdited"),
        follow_redirects=True,
    )
    assert b"You do not have permission" not in response.data
    assert b"Success!" in response.data

    # dont have access to delete
    response: Response = client.post(
        f"/book/{book.id}/delete",
        data=dict(book_id=book.id),
        follow_redirects=True,
    )
    assert b"You do not have permission" in response.data

    # access to create collection
    collection, response = create_collection(client, book.id)
    assert b"You do not have permission" not in response.data
    assert b"Success!" in response.data

    # access to edit collection
    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/edit",
        data=dict(label="NewLabel"),
        follow_redirects=True,
    )
    assert b"You do not have permission" not in response.data
    assert b"Success!" in response.data

    # access to delete collection
    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/delete", follow_redirects=True
    )
    assert b"You do not have permission" not in response.data
    assert b"Success!" in response.data

    # restore collection
    collection.is_deleted = False
    collection.save()

    # access to create section
    section, response = create_section(client, book.id, collection.id)
    assert b"You do not have permission" not in response.data
    assert b"Success!" in response.data

    # access to edit section
    response: Response = client.post(
        f"/book/{book.id}/{section.id}/edit_section",
        data=dict(section_id=section.id, label="NewLabel"),
        follow_redirects=True,
    )
    assert b"You do not have permission" not in response.data
    assert b"Success!" in response.data

    # access to delete section
    response: Response = client.post(
        f"/book/{book.id}/{section.id}/delete_section", follow_redirects=True
    )
    assert b"You do not have permission" not in response.data
    assert b"Success!" in response.data

    # restore section
    section.is_deleted = False
    section.save()

    # access to create interpretation
    interpretation, response = create_interpretation(client, book.id, section.id)
    assert b"You do not have permission" not in response.data
    assert b"Success!" in response.data

    # access to approve interpretation
    response: Response = client.post(
        f"/approve/interpretation/{interpretation.id}",
        follow_redirects=True,
    )

    assert response
    assert response.json["message"] == "success"
    assert response.json["approve"]
    assert interpretation.approved

    # access to delete interpretation
    response: Response = client.post(
        f"/book/{book.id}/{interpretation.id}/delete_interpretation",
        data=dict(interpretation_id=interpretation.id),
        follow_redirects=True,
    )
    assert b"You do not have permission" not in response.data
    assert b"Success!" in response.data

    # restore interpretation
    interpretation.is_deleted = False
    interpretation.save()

    # access to create comment
    comment, response = create_comment(client, book.id, interpretation.id)
    assert b"You do not have permission" not in response.data
    assert b"Success!" in response.data

    # access to approve comment
    response: Response = client.post(
        f"/approve/comment/{comment.id}",
        follow_redirects=True,
    )

    assert response
    assert response.json["message"] == "success"
    assert response.json["approve"]
    assert interpretation.approved

    # access to delete comment
    response: Response = client.post(
        f"/book/{book.id}/{interpretation.id}/comment_delete",
        data=dict(
            text=comment.text,
            interpretation_id=interpretation.id,
            comment_id=comment.id,
        ),
        follow_redirects=True,
    )
    assert b"You do not have permission" not in response.data
    assert b"Success!" in response.data


def test_moderator_access_to_entire_book(client):
    login(client)
    book = create_book(client)

    editor = m.User(username="moderator", password="moderator").save()
    response: Response = client.post(
        f"/book/{book.id}/add_contributor",
        data=dict(user_id=editor.id, role=m.BookContributor.Roles.MODERATOR),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Contributor was added!" in response.data

    logout(client)
    login(client, "moderator", "moderator")

    # access to settings page
    response: Response = client.get(f"/book/{book.id}/settings", follow_redirects=True)
    assert b"You do not have permission" in response.data

    # access to edit book
    response: Response = client.post(
        f"/book/{book.id}/edit",
        data=dict(book_id=book.id, label="BookEdited"),
        follow_redirects=True,
    )
    assert b"You do not have permission" in response.data

    # dont have access to delete
    response: Response = client.post(
        f"/book/{book.id}/delete",
        data=dict(book_id=book.id),
        follow_redirects=True,
    )
    assert b"You do not have permission" in response.data

    logout(client)
    login(client)
    collection, response = create_collection(client, book.id)
    section, response = create_section(client, book.id, collection.id)
    login(client, "moderator", "moderator")

    # access to create interpretation
    interpretation, response = create_interpretation(client, book.id, section.id)
    assert b"You do not have permission" not in response.data
    assert b"Success!" in response.data

    # access to approve interpretation
    response: Response = client.post(
        f"/approve/interpretation/{interpretation.id}",
        follow_redirects=True,
    )

    assert response
    assert response.json["message"] == "success"
    assert response.json["approve"]
    assert interpretation.approved

    # access to delete interpretation
    response: Response = client.post(
        f"/book/{book.id}/{interpretation.id}/delete_interpretation",
        data=dict(interpretation_id=interpretation.id),
        follow_redirects=True,
    )
    assert b"You do not have permission" not in response.data
    assert b"Success!" in response.data

    # restore interpretation
    interpretation.is_deleted = False
    interpretation.save()

    # access to create comment
    comment, response = create_comment(client, book.id, interpretation.id)
    assert b"You do not have permission" not in response.data
    assert b"Success!" in response.data

    # access to approve comment
    response: Response = client.post(
        f"/approve/comment/{comment.id}",
        follow_redirects=True,
    )

    assert response
    assert response.json["message"] == "success"
    assert response.json["approve"]
    assert interpretation.approved

    # access to delete comment
    response: Response = client.post(
        f"/book/{book.id}/{interpretation.id}/comment_delete",
        data=dict(
            text=comment.text,
            interpretation_id=interpretation.id,
            comment_id=comment.id,
        ),
        follow_redirects=True,
    )
    assert b"You do not have permission" not in response.data
    assert b"Success!" in response.data


def test_editor_access_tree_entire_book(client):
    login(client)
    book = create_book(client)
    collection_1, _ = create_collection(client, book.id)
    collection_2, _ = create_collection(client, book.id)

    editor = m.User(username="editor", password="editor").save()
    response: Response = client.post(
        f"/book/{book.id}/add_contributor",
        data=dict(user_id=editor.id, role=m.BookContributor.Roles.EDITOR),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Contributor was added!" in response.data

    response: Response = client.get(
        f"/permission/access_tree?user_id={editor.id}&book_id={book.id}",
        follow_redirects=True,
    )
    assert response.status_code == 200
    json = response.json
    access_tree = json.get("access_tree")
    assert access_tree
    assert book.id in access_tree.get("book")
    collections_ids = access_tree.get("collection")
    assert collections_ids
    assert collection_1.id in collections_ids
    assert collection_2.id in collections_ids


def test_set_access_level(client):
    login(client)
    book = create_book(client)
    collection_1, _ = create_collection(client, book.id)
    collection_2, _ = create_collection(client, book.id)

    editor = m.User(username="editor", password="editor").save()
    response: Response = client.post(
        f"/book/{book.id}/add_contributor",
        data=dict(user_id=editor.id, role=m.BookContributor.Roles.EDITOR),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Contributor was added!" in response.data
    assert len(book.list_access_groups) == 2

    json_string = json.dumps({"collection": [collection_1.id]})
    response: Response = client.post(
        "/permission/set",
        data=dict(
            book_id=book.id,
            user_id=editor.id,
            permissions=json_string,
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert len(book.list_access_groups) == 3

    response: Response = client.post(
        "/permission/set",
        data=dict(
            book_id=book.id,
            user_id=editor.id,
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Success!" not in response.data
