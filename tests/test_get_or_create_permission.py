from app import models as m
from app.controllers.get_or_create_permission import get_or_create_permission


def test_get_or_create_permission(client):
    access = m.Permission.Access
    entity_type = m.Permission.Entity

    book_u: m.Permission = m.Permission.query.filter_by(
        access=access.U, entity_type=entity_type.BOOK
    ).first()
    assert not book_u

    assert not m.Permission.query.count()

    book_u: m.Permission = get_or_create_permission(
        access=access.U, entity_type=entity_type.BOOK
    )
    assert book_u
    assert book_u.access == access.U
    assert book_u.entity_type == entity_type.BOOK
    assert m.Permission.query.count() == 1

    book_u: m.Permission = m.Permission.query.filter_by(
        access=access.U, entity_type=entity_type.BOOK
    ).first()
    assert book_u
    assert book_u.access == access.U
    assert book_u.entity_type == entity_type.BOOK

    get_or_create_permission(access=access.U, entity_type=entity_type.BOOK)
    assert m.Permission.query.count() == 1
