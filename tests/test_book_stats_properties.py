from flask.testing import FlaskClient

from app import models as m
from tests.utils import login, create_test_book


def test_approved_interpretations(client: FlaskClient):
    _, user = login(client)
    create_test_book(user.id)

    dummy_user = m.User(username="Bob").save()
    create_test_book(dummy_user.id)

    book: m.Book = m.Book.query.first()

    assert len(book.approved_interpretations) == 0

    for interpretation in m.Interpretation.query.all():
        interpretation.approved = True
        interpretation.save()

    assert len(book.approved_interpretations) == 1

    section: m.Section = m.Section.query.first()
    assert section
    interpretation: m.Interpretation = m.Interpretation(
        section_id=section.id, label="231", text="123", approved=True
    ).save()

    assert len(book.approved_interpretations) == 2

    interpretation.is_deleted = True
    interpretation.save()

    assert len(book.approved_interpretations) == 1

    collection: m.Collection = m.Collection.query.first()
    sub_collection: m.Collection = m.Collection(
        parent_id=collection.id,
        label="123",
    ).save()
    section: m.Section = m.Section(
        label="123", collection_id=sub_collection.id, version_id=book.last_version.id
    ).save()
    interpretation: m.Interpretation = m.Interpretation(
        section_id=section.id, label="231", text="123", approved=True
    ).save()

    assert len(book.approved_interpretations) == 2

    sub_collection.is_deleted = True
    sub_collection.save()
    assert len(book.approved_interpretations) == 1

    sub_collection.is_deleted = False
    sub_collection.save()
    assert len(book.approved_interpretations) == 2

    # collection.is_deleted = True
    # collection.save()
    # assert len(book.approved_interpretations) == 0


def test_approved_comments(client: FlaskClient):
    _, user = login(client)
    create_test_book(user.id)

    dummy_user = m.User(username="Bob").save()
    create_test_book(dummy_user.id)

    book: m.Book = m.Book.query.first()

    assert len(book.approved_comments) == 0

    for comment in m.Comment.query.all():
        comment.approved = True
        comment.save()

    assert len(book.approved_comments) == 1

    interpretation: m.Interpretation = m.Interpretation.query.first()
    assert interpretation
    comment: m.Comment = m.Comment(
        text="231", approved=True, interpretation_id=interpretation.id
    ).save()

    assert len(book.approved_comments) == 2

    comment.is_deleted = True
    comment.save()

    assert len(book.approved_comments) == 1

    comment: m.Comment = m.Comment(
        text="456", approved=True, interpretation_id=interpretation.id
    ).save()

    assert len(book.approved_comments) == 2

    interpretation.is_deleted = True
    interpretation.save()
    assert len(book.approved_comments) == 0

    interpretation.is_deleted = False
    interpretation.save()
    assert len(book.approved_comments) == 2

    collection: m.Collection = m.Collection.query.first()
    collection.is_deleted = True
    collection.save()

    interpretation.is_deleted = False
    interpretation.save()
    assert len(book.approved_comments) == 0
