from random import randint

from flask import current_app as Response, url_for
from flask.testing import FlaskClient, FlaskCliRunner

from app import models as m, db
from app.controllers.create_access_groups import create_moderator_group
from tests.utils import (
    login,
    logout,
    check_if_nested_book_entities_is_deleted,
    check_if_nested_collection_entities_is_deleted,
    check_if_nested_section_entities_is_deleted,
    check_if_nested_interpretation_entities_is_deleted,
    create_test_book,
)


def create_book(client):
    random_id = randint(1, 100)
    BOOK_NAME = f"TBook {random_id}"
    response: Response = client.post(
        "/book/create",
        data=dict(label=BOOK_NAME),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Book added!" in response.data

    book: m.Book = m.Book.query.filter_by(label=BOOK_NAME).first()

    assert book
    assert book.versions
    assert len(book.versions) == 1
    assert book.access_groups
    assert len(book.access_groups) == 2

    root_collection: m.Collection = book.last_version.collections[0]
    assert root_collection
    assert root_collection.access_groups
    assert len(root_collection.access_groups) == 2

    return book


def create_collection(client, book_id):
    random_id = randint(1, 100)
    LABEL = f"TCollection {random_id}"
    response: Response = client.post(
        f"/book/{book_id}/create_collection",
        data=dict(label=LABEL),
        follow_redirects=True,
    )

    assert response.status_code == 200
    collection: m.Collection = m.Collection.query.filter_by(label=LABEL).first()

    return collection, response


def create_section(client, book_id, collection_id):
    random_id = randint(1, 100)
    LABEL = f"TSection {random_id}"
    response: Response = client.post(
        f"/book/{book_id}/{collection_id}/create_section",
        data=dict(collection_id=collection_id, label=LABEL),
        follow_redirects=True,
    )

    section: m.Section = m.Section.query.filter_by(
        label=LABEL, collection_id=collection_id
    ).first()
    return section, response


def create_interpretation(client, book_id, section_id):
    random_id = randint(1, 100)
    LABEL = f"TInterpretation {random_id}"
    response: Response = client.post(
        f"/book/{book_id}/{section_id}/create_interpretation",
        data=dict(section_id=section_id, text=LABEL),
        follow_redirects=True,
    )
    interpretation: m.Interpretation = m.Interpretation.query.filter_by(
        section_id=section_id, text=LABEL
    ).first()
    return interpretation, response


def create_comment(client, book_id, interpretation_id):
    random_id = randint(1, 100)
    TEXT = f"TComment {random_id}"
    response: Response = client.post(
        f"/book/{book_id}/{interpretation_id}/create_comment",
        data=dict(
            text=TEXT,
            interpretation_id=interpretation_id,
        ),
        follow_redirects=True,
    )
    comment: m.Comment = m.Comment.query.filter_by(text=TEXT).first()
    return comment, response


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
        (f"/book/{book.id}/{interpretation.id}/delete_interpretation"),
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
        (f"/book/{book.id}/{interpretation.id}/delete_interpretation"),
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
