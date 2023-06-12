from flask.testing import FlaskClient
from flask import current_app as Response

from app.controllers.jinja_globals import (
    build_qa_url_using_interpretation,
)
from .utils import (
    create_book,
    login,
    create_collection,
    create_section,
    create_interpretation,
    create_comment,
)
from app import models as m


def test_build_qa_url_using_interpretation(client: FlaskClient):
    login(client)

    book = create_book(client)
    collection, _ = create_collection(client, book.id)
    section, _ = create_section(client, book.id, collection.id)
    interpretation, _ = create_interpretation(client, book.id, section.id)
    create_comment(client, book.id, interpretation.id)

    interpretation: m.Interpretation = m.Interpretation.query.first()

    url = build_qa_url_using_interpretation(interpretation)
    assert url

    response: Response = client.get(url, follow_redirects=True)
    assert response.status_code == 200

    section: m.Section = m.Section.query.first()
    assert section
    assert str.encode(section.label) in response.data
