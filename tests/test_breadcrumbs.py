from flask.testing import FlaskCliRunner
from app.controllers import create_breadcrumbs
from app import models as m, db


def test_breadcrumbs(runner: FlaskCliRunner, app):
    runner.invoke(args=["db-populate"])
    with app.app_context(), app.test_request_context():
        res = create_breadcrumbs(book_id=1, collection_id=1, section_id=1)
    assert len(res) == 4
    book: m.Book = db.session.get(m.Book, 1)
    assert book
    assert book.owner.username in res[0].label
    assert res[1].label == book.label
    with app.app_context(), app.test_request_context():
        res = create_breadcrumbs(book_id=1, section_id=1)
    assert res
    assert len(res) == 4
