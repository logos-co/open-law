from app.controllers import create_breadcrumbs
from app import models as m, db
from tests.utils import create_book, login, create_collection, create_section


def test_breadcrumbs(client, app):
    login(client)
    book = create_book(client)
    collection, _ = create_collection(client, book.id)
    section, _ = create_section(client, book.id, collection.id)
    with app.app_context(), app.test_request_context():
        res = create_breadcrumbs(
            book_id=book.id, collection_id=collection.id, section_id=section.id
        )
    assert len(res) == 4
    book: m.Book = db.session.get(m.Book, 1)
    assert book
    assert book.owner.username in res[0].label
    assert res[1].label == book.label
    with app.app_context(), app.test_request_context():
        res = create_breadcrumbs(book_id=1, section_id=1)
    assert res
    assert len(res) == 4
