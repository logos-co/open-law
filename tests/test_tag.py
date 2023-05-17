from flask import current_app as Response
from flask.testing import FlaskClient

from app import models as m, db
from tests.utils import login, create_test_book


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

    splitted_tags = [tag.title() for tag in tags.split(",")]
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


def test_create_tags_on_comment_create_and_edit(client: FlaskClient):
    _, user = login(client)
    create_test_book(user.id, 1)

    book = db.session.get(m.Book, 1)
    collection = db.session.get(m.Collection, 1)
    section = db.session.get(m.Section, 1)
    interpretation = db.session.get(m.Interpretation, 1)

    tags = "tag1,tag2,tag3"
    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/{section.id}/{interpretation.id}/create_comment",
        data=dict(
            section_id=section.id,
            text="some text",
            interpretation_id=interpretation.id,
            tags=tags,
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200

    comment: m.Comment = m.Comment.query.filter_by(text="some text").first()
    assert comment
    assert comment.tags

    splitted_tags = [tag.title() for tag in tags.split(",")]
    assert len(comment.tags) == 3
    for tag in comment.tags:
        tag: m.Tag
        assert tag.name in splitted_tags

    tags_from_db: m.Tag = m.Tag.query.all()
    assert len(tags_from_db) == 3

    tags = "tag1,tag5,tag7"
    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/{section.id}/{interpretation.id}/comment_edit",
        data=dict(text=comment.text, tags=tags, comment_id=comment.id),
        follow_redirects=True,
    )
    assert response.status_code == 200

    comment: m.Comment = m.Comment.query.filter_by(text="some text").first()
    assert comment
    assert comment.tags

    splitted_tags = [tag.title() for tag in tags.split(",")]
    assert len(comment.tags) == 3
    for tag in comment.tags:
        tag: m.Tag
        assert tag.name in splitted_tags

    tags_from_db: m.Tag = m.Tag.query.all()
    assert len(tags_from_db) == 5


def test_create_tags_on_interpretation_create_and_edit(client: FlaskClient):
    _, user = login(client)
    create_test_book(user.id, 1)

    book = db.session.get(m.Book, 1)
    collection = db.session.get(m.Collection, 1)
    section = db.session.get(m.Section, 1)

    tags = "tag1,tag2,tag3"
    label_1 = "Test Interpretation #1 Label"
    text_1 = "Test Interpretation #1 Text"

    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/{section.id}/create_interpretation",
        data=dict(section_id=section.id, label=label_1, text=text_1, tags=tags),
        follow_redirects=True,
    )

    assert response.status_code == 200
    interpretation: m.Interpretation = m.Interpretation.query.filter_by(
        label=label_1, section_id=section.id
    ).first()
    assert interpretation
    assert interpretation.tags

    splitted_tags = [tag.title() for tag in tags.split(",")]
    assert len(interpretation.tags) == 3
    for tag in interpretation.tags:
        tag: m.Tag
        assert tag.name in splitted_tags

    tags_from_db: m.Tag = m.Tag.query.all()
    assert len(tags_from_db) == 3

    tags = "tag-4,tag5,tag3"
    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/{section.id}/{interpretation.id}/edit_interpretation",
        data=dict(
            interpretation_id=interpretation.id, label=label_1, text=text_1, tags=tags
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    interpretation: m.Interpretation = m.Interpretation.query.filter_by(
        label=label_1, section_id=section.id
    ).first()
    assert interpretation

    splitted_tags = [tag.title() for tag in tags.split(",")]
    assert len(interpretation.tags) == 3
    for tag in interpretation.tags:
        tag: m.Tag
        assert tag.name in splitted_tags

    tags_from_db: m.Tag = m.Tag.query.all()
    assert len(tags_from_db) == 5


def test_create_tags_on_section_create_and_edit(client: FlaskClient):
    _, user = login(client)
    create_test_book(user.id, 1)

    book: m.Book = db.session.get(m.Book, 1)
    collection: m.Collection = db.session.get(m.Collection, 1)
    section: m.Section = db.session.get(m.Section, 1)

    tags = "tag1,tag2,tag3"
    label_1 = "Test Interpretation #1 Label"
    text_1 = "Test Interpretation #1 Text"

    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/create_section",
        data=dict(
            collection_id=collection.id,
            label=label_1,
            about=text_1,
            tags=tags,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200

    assert response.status_code == 200
    section: m.Section = m.Section.query.filter_by(label=label_1).first()
    assert section
    assert section.tags

    splitted_tags = [tag.title() for tag in tags.split(",")]
    assert len(section.tags) == 3
    for tag in section.tags:
        tag: m.Tag
        assert tag.name in splitted_tags

    tags_from_db: m.Tag = m.Tag.query.all()
    assert len(tags_from_db) == 3

    tags = "tag-4,tag5,tag3"
    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/{section.id}/edit_section",
        data=dict(
            section_id=section.id,
            label=label_1,
            about=text_1,
            tags=tags,
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Success!" in response.data

    assert response.status_code == 200
    section: m.Section = m.Section.query.filter_by(label=label_1).first()
    assert section
    assert section.tags

    splitted_tags = [tag.title() for tag in tags.split(",")]
    assert len(section.tags) == 3
    for tag in section.tags:
        tag: m.Tag
        assert tag.name in splitted_tags

    tags_from_db: m.Tag = m.Tag.query.all()
    assert len(tags_from_db) == 5
