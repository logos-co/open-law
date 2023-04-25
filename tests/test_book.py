from flask import current_app as Response
from flask.testing import FlaskClient, FlaskCliRunner

from app import models as m, db
from tests.utils import login


def test_create_book(client: FlaskClient):
    login(client)

    BOOK_NAME = "Test Book"

    # label len < 6
    response: Response = client.post(
        "/book/create",
        data=dict(
            label="12345",
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Label must be between 6 and 1024 characters long." in response.data

    book = m.Book.query.filter_by(label=BOOK_NAME).first()

    assert not book
    assert not m.Book.query.count()

    # label len > 1024
    response: Response = client.post(
        "/book/create",
        data=dict(
            label="".join(["0" for _ in range(1025)]),
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Label must be between 6 and 1024 characters long." in response.data

    book = m.Book.query.filter_by(label=BOOK_NAME).first()

    assert not book
    assert not m.Book.query.count()

    response: Response = client.post(
        "/book/create",
        data=dict(
            label=BOOK_NAME,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Book added!" in response.data

    book = m.Book.query.filter_by(label=BOOK_NAME).first()

    assert book
    assert book.versions
    assert len(book.versions) == 1


def test_add_contributor(client: FlaskClient):
    _, user = login(client)
    user: m.User

    moderator = m.User(username="Moderator", password="test").save()

    moderators_book = m.Book(label="Test Book", user_id=moderator.id).save()
    response: Response = client.post(
        f"/book/{moderators_book.id}/add_contributor",
        data=dict(user_id=moderator.id, role=m.BookContributor.Roles.MODERATOR),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"You are not owner of this book!" in response.data

    book = m.Book(label="Test Book", user_id=user.id).save()

    response: Response = client.post(
        f"/book/{book.id}/add_contributor",
        data=dict(user_id=moderator.id, role=m.BookContributor.Roles.MODERATOR),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Contributor was added!" in response.data
    response: Response = client.post(
        f"/book/{book.id}/add_contributor",
        data=dict(user_id=moderator.id, role=m.BookContributor.Roles.MODERATOR),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Already exists!" in response.data

    contributor: m.BookContributor = m.BookContributor.query.filter_by(
        user=moderator, book=book
    ).first()
    assert contributor.role == m.BookContributor.Roles.MODERATOR
    assert len(book.contributors) == 1

    editor = m.User(username="Editor", password="test").save()
    response: Response = client.post(
        f"/book/{book.id}/add_contributor",
        data=dict(user_id=editor.id, role=m.BookContributor.Roles.EDITOR),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Contributor was added!" in response.data

    contributor: m.BookContributor = m.BookContributor.query.filter_by(
        user=editor, book=book
    ).first()
    assert contributor.role == m.BookContributor.Roles.EDITOR
    assert len(book.contributors) == 2


def test_delete_contributor(client: FlaskClient, runner: FlaskCliRunner):
    _, user = login(client)
    user: m.User

    # add dummmy data
    runner.invoke(args=["db-populate"])

    book = db.session.get(m.Book, 1)
    book.user_id = user.id
    book.save()

    contributors_len = len(book.contributors)
    assert contributors_len

    contributor_to_delete = book.contributors[0]

    response: Response = client.post(
        f"/book/{book.id}/delete_contributor",
        data=dict(user_id=contributor_to_delete.user_id),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Success!" in response.data

    response: Response = client.post(
        f"/book/{book.id}/delete_contributor",
        data=dict(user_id=contributor_to_delete.user_id),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Does not exists!" in response.data
