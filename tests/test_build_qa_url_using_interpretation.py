from flask.testing import FlaskClient
from flask import current_app as Response

from app.controllers.jinja_globals import (
    build_qa_url_using_interpretation,
)
from .utils import create_test_book, login
from app import models as m


def test_build_qa_url_using_interpretation(client: FlaskClient):
    _, user = login(client)
    user: m.User

    create_test_book(user.id)

    interpretation: m.Interpretation = m.Interpretation.query.first()

    url = build_qa_url_using_interpretation(interpretation)
    assert url

    response: Response = client.get(url, follow_redirects=True)
    assert response.status_code == 200

    section: m.Section = m.Section.query.first()
    assert section
    assert str.encode(section.label) in response.data
