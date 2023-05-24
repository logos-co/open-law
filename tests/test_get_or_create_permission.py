from app import models as m
from app.controllers.get_or_create_permission import get_or_create_permission


def test_get_or_create_permission(client):
    access = m.Permission.Access
    entity = m.Permission.Entity

    book_u: m.Permission = m.Permission.query.filter_by(
        access=access.U, entity=entity.BOOK
    ).first()
    assert not book_u

    assert not m.Permission.query.count()

    book_u: m.Permission = get_or_create_permission(access=access.U, entity=entity.BOOK)
    assert book_u
    assert book_u.access == access.U
    assert book_u.entity == entity.BOOK
    assert m.Permission.query.count() == 1

    book_u: m.Permission = m.Permission.query.filter_by(
        access=access.U, entity=entity.BOOK
    ).first()
    assert book_u
    assert book_u.access == access.U
    assert book_u.entity == entity.BOOK

    get_or_create_permission(access=access.U, entity=entity.BOOK)
    assert m.Permission.query.count() == 1
