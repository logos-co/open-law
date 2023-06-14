from flask import current_app as Response
from flask.testing import FlaskClient

from app import models as m
from tests.utils import (
    login,
    logout,
    create_book,
)


def test_fork_book(client: FlaskClient):
    login(client)

    book: m.Book = create_book(client)
    assert book
    assert len(book.forks) == 0

    logout(client)
    _, user = login(client, "Test_U")

    response: Response = client.post(
        f"/book/{book.id}/fork",
        data=dict(
            label="Label",
            about="About",
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Success" in response.data
    assert len(book.forks) == 1

    assert user.books
    fork = user.books[0]
    assert fork.original_book_id == book.id
    assert fork.user_id != book.user_id
