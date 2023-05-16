# flake8: noqa F501
from flask import current_app as Response
from flask.testing import FlaskClient, FlaskCliRunner

from app import models as m, db
from tests.utils import login, logout


def test_create_tags_on_book_edit(client: FlaskClient):
    _, user = login(client)

    book: m.Book = m.Book(label="Test book", user_id=user.id).save()
    m.BookVersion = m.BookVersion(semver="1.0.0", book_id=book.id).save()

    assert not book.tags

    tags = "tag1,tag2,tag3"

    client.post(
        f"/book/{book.id}/edit",
        data=dict(book_id=book.id, label=book.label, tags=tags),
        follow_redirects=True,
    )

    book: m.Book = m.Book.query.first()

    splitted_tags = [tag.title() for tag in tags.split(",")]
    assert len(book.tags) == 3
    for tag in book.tags:
        tag: m.Tag
        assert tag.name in splitted_tags

    tags_from_db: m.Tag = m.Tag.query.all()
    assert len(tags_from_db) == 3

    tags = "tag1,tag2,tag4"

    client.post(
        f"/book/{book.id}/edit",
        data=dict(book_id=book.id, label=book.label, tags=tags),
        follow_redirects=True,
    )

    tags_from_db: m.Tag = m.Tag.query.all()
    assert len(tags_from_db) == 4
    book: m.Book = m.Book.query.first()
    assert len(book.tags) == 3

    tags = "1" * 33

    client.post(
        f"/book/{book.id}/edit",
        data=dict(book_id=book.id, label=book.label, tags=tags),
        follow_redirects=True,
    )

    tags_from_db: m.Tag = m.Tag.query.all()
    assert len(tags_from_db) == 4
    book: m.Book = m.Book.query.first()
    assert len(book.tags) == 0
