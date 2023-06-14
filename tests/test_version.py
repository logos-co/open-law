from flask import current_app as Response
from flask.testing import FlaskClient

from app import models as m, db
from tests.utils import (
    login,
    logout,
    create_book,
    check_if_nested_version_entities_is_deleted,
)


def test_edit_version(client: FlaskClient):
    login(client)

    book: m.Book = create_book(client)
    book_2: m.Book = create_book(client)
    assert book
    assert len(book.versions) == 1
    version: m.BookVersion = book.versions[0]

    new_semver = f"{version.semver} EDITED"

    response: Response = client.post(
        f"/book/{book.id}/edit_version",
        data=dict(
            version_id=version.id,
            semver=new_semver,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Success" in response.data
    assert version.semver == new_semver

    response: Response = client.post(
        f"/book/{book.id}/edit_version",
        data=dict(
            version_id=version.id,
            semver=new_semver,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Version name must me unique" in response.data

    response: Response = client.post(
        f"/book/{book.id}/edit_version",
        data=dict(
            version_id=0,
            semver=new_semver,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Version not found" in response.data

    response: Response = client.post(
        f"/book/{book.id}/edit_version",
        data=dict(
            version_id=book_2.versions[0].id,
            semver="Test",
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid version id" in response.data

    logout(client)
    login(client, username="test_user")

    response: Response = client.post(
        f"/book/{book.id}/edit_version",
        data=dict(
            version_id=book_2.versions[0].id,
            semver="Test",
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"You are not owner of this book" in response.data


def test_delete_version(client: FlaskClient):
    login(client)

    book: m.Book = create_book(client)
    book_2: m.Book = create_book(client)
    assert book
    assert len(book.versions) == 1
    version: m.BookVersion = book.versions[0]

    response: Response = client.post(
        f"/book/{book.id}/delete_version",
        data=dict(
            version_id=version.id,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"You cant delete active version" in response.data

    response: Response = client.post(
        f"/book/{book.id}/delete_version",
        data=dict(
            version_id=0,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Version not found" in response.data

    response: Response = client.post(
        f"/book/{book.id}/delete_version",
        data=dict(
            version_id=book_2.versions[0].id,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid version id" in response.data

    response: Response = client.post(
        f"/book/{book_2.id}/create_version",
        data=dict(
            semver="MyVer",
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Success" in response.data
    assert len(book_2.versions) == 2

    new_version: m.BookVersion = book_2.versions[-1]

    for collection in new_version.root_collection.active_children:
        recursive_copy_collection(collection)

    response: Response = client.post(
        f"/book/{book_2.id}/delete_version",
        data=dict(
            version_id=new_version.id,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Success" in response.data
    check_if_nested_version_entities_is_deleted(new_version)

    logout(client)
    login(client, username="test_user")

    response: Response = client.post(
        f"/book/{book.id}/delete_version",
        data=dict(
            version_id=book_2.versions[0].id,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"You are not owner of this book" in response.data


def recursive_copy_collection(collection: m.Collection):
    collection: m.Collection
    assert collection.copy_of

    copy_of: m.Collection = db.session.get(m.Collection, collection.copy_of)
    assert collection.label == copy_of.label
    assert collection.about == copy_of.about
    assert collection.is_root == copy_of.is_root
    assert collection.is_leaf == copy_of.is_leaf
    assert collection.position == copy_of.position

    if collection.active_sections:
        for section in collection.active_sections:
            section: m.Section
            copy_of = db.session.get(m.Section, section.copy_of)
            assert section.label == copy_of.label
            assert section.position == copy_of.position

            interpretations: list[m.Interpretation] = section.approved_interpretation
            for interpretation in interpretations:
                interpretation: m.Interpretation
                assert interpretation.copy_of

                copy_of: m.Interpretation = db.session.get(
                    m.Interpretation, interpretation.copy_of
                )
                assert interpretation.text == copy_of.text
                assert interpretation.plain_text == copy_of.plain_text
                assert interpretation.approved == copy_of.approved

            comments: list[m.Comment] = section.approved_comments
            for comment in comments:
                comment: m.Comment
                assert comment.copy_of

                copy_of: m.Comment = db.session.get(m.Comment, comment.copy_of)
                assert comment.text == copy_of.text
                assert comment.approved == copy_of.approved
                assert comment.edited == copy_of.edited

    elif collection.active_children:
        for child in collection.active_children:
            recursive_copy_collection(child)


def test_create_version(client):
    login(client)

    book: m.Book = create_book(client)

    logout(client)
    login(client, "test_2")

    response: Response = client.post(
        f"/book/{book.id}/create_version",
        data=dict(
            semver="MyVer",
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"You are not owner of this book" in response.data

    logout(client)
    login(client)

    response: Response = client.post(
        f"/book/{book.id}/create_version",
        data=dict(
            semver="MyVer",
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Success" in response.data
    assert len(book.versions) == 2

    new_version: m.BookVersion = book.versions[-1]

    for collection in new_version.root_collection.active_children:
        recursive_copy_collection(collection)
