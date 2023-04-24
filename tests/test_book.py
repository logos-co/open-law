from flask import current_app as Response
from flask.testing import FlaskClient

from app import models as m
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


# def test_add_c(client: FlaskClient):
#     login(client)


#     response: Response = client.post(
#         "/book/create",
#         data=dict(
#             label=BOOK_NAME,
#         ),
#         follow_redirects=True,
#     )

#     assert response.status_code == 200
#     assert b"Book added!" in response.data

#     book = m.Book.query.filter_by(label=BOOK_NAME).first()

#     assert book
