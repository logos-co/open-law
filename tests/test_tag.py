from flask import current_app as Response
from flask.testing import FlaskClient

from app import models as m
from tests.utils import (
    create_book,
    create_collection,
    create_comment,
    create_interpretation,
    create_section,
    login,
)


def test_create_tags_on_book_create_and_edit(client: FlaskClient):
    login(client)

    BOOK_NAME = "Test Book"
    tags = "tag1,tag2,tag3"

    response: Response = client.post(
        "/book/create",
        data=dict(label=BOOK_NAME, tags=tags),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Book added!" in response.data

    book = m.Book.query.filter_by(label=BOOK_NAME).first()
    assert book.tags

    splitted_tags = [tag.lower() for tag in tags.split(",")]
    assert len(book.tags) == 3
    for tag in book.tags:
        tag: m.Tag
        assert tag.name in splitted_tags

    tags_from_db: m.Tag = m.Tag.query.all()
    assert len(tags_from_db) == 3

    tags = "tag1,tag2,tag3"

    client.post(
        f"/book/{book.id}/edit",
        data=dict(book_id=book.id, label=book.label, tags=tags),
        follow_redirects=True,
    )

    book: m.Book = m.Book.query.first()

    splitted_tags = [tag.lower() for tag in tags.split(",")]
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


def test_create_tags_on_comment_create_and_edit(client: FlaskClient):
    login(client)
    book = create_book(client)
    collection, _ = create_collection(client, book.id)
    section, _ = create_section(client, book.id, collection.id)
    interpretation, _ = create_interpretation(client, book.id, section.id)
    comment, _ = create_comment(client, book.id, interpretation.id)

    tags = "#tag1 #tag2 #tag3"
    response: Response = client.post(
        f"/book/{book.id}/{interpretation.id}/create_comment",
        data=dict(
            section_id=section.id,
            text="some text" + tags,
            interpretation_id=interpretation.id,
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200

    comment: m.Comment = m.Comment.query.filter_by(text="some text" + tags).first()
    assert comment
    assert comment.tags

    splitted_tags = [tag.lower().replace("#", "") for tag in tags.split()]
    assert len(comment.tags) == 3
    for tag in comment.tags:
        tag: m.Tag
        assert tag.name in splitted_tags

    tags_from_db: m.Tag = m.Tag.query.all()
    assert len(tags_from_db) == 3

    tags = "#tag1 #tag5 #tag7"
    response: Response = client.post(
        f"/book/{book.id}/{interpretation.id}/comment_edit",
        data=dict(text="some text" + tags, comment_id=comment.id),
        follow_redirects=True,
    )
    assert response.status_code == 200

    comment: m.Comment = m.Comment.query.filter_by(text="some text" + tags).first()
    assert comment
    assert comment.tags

    splitted_tags = [tag.lower().replace("#", "") for tag in tags.split()]
    assert len(comment.tags) == 3
    for tag in comment.tags:
        tag: m.Tag
        assert tag.name in splitted_tags

    tags_from_db: m.Tag = m.Tag.query.all()
    assert len(tags_from_db) == 5


def test_create_tags_on_interpretation_create_and_edit(client: FlaskClient):
    login(client)
    book = create_book(client)
    collection, _ = create_collection(client, book.id)
    section, _ = create_section(client, book.id, collection.id)
    interpretation, _ = create_interpretation(client, book.id, section.id)

    tags = "#tag1 #tag2 #tag3"
    text_1 = "Test Interpretation no1 Text"

    response: Response = client.post(
        f"/book/{book.id}/{section.id}/create_interpretation",
        data=dict(section_id=section.id, text=text_1 + tags),
        follow_redirects=True,
    )

    assert response.status_code == 200
    interpretation: m.Interpretation = m.Interpretation.query.filter_by(
        text=text_1 + tags, section_id=section.id
    ).first()
    assert interpretation
    assert interpretation.tags

    splitted_tags = [tag.lower().replace("#", "") for tag in tags.split()]
    assert len(interpretation.tags) == 3
    for tag in interpretation.tags:
        tag: m.Tag
        assert tag.name in splitted_tags

    tags_from_db: m.Tag = m.Tag.query.all()
    assert len(tags_from_db) == 3

    tags = "#tag4 #tag3 #tag5"
    response: Response = client.post(
        f"/book/{book.id}/{interpretation.id}/edit_interpretation",
        data=dict(interpretation_id=interpretation.id, text=text_1 + tags),
        follow_redirects=True,
    )

    assert response.status_code == 200
    interpretation: m.Interpretation = m.Interpretation.query.filter_by(
        text=text_1 + tags, section_id=section.id
    ).first()
    assert interpretation

    splitted_tags = [tag.lower().replace("#", "") for tag in tags.split()]
    assert len(interpretation.tags) == 3
    for tag in interpretation.tags:
        tag: m.Tag
        assert tag.name in splitted_tags

    tags_from_db: m.Tag = m.Tag.query.all()
    assert len(tags_from_db) == 5
