from flask import current_app as Response
from flask.testing import FlaskClient, FlaskCliRunner

from app import models as m, db
from app.controllers.create_access_groups import create_moderator_group
from tests.utils import (
    login,
    logout,
    create_book,
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

    # TODO improve test to check if nested items are deleted
    # response: Response = client.post(
    #     f"/book/{book.id}/delete_version",
    #     data=dict(
    #         version_id=book_2.versions[0].id,
    #     ),
    #     follow_redirects=True,
    # )

    # assert response.status_code == 200
    # assert b"Success" in response.data

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
