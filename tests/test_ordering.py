from flask import current_app as Response

from app import models as m, db
from tests.utils import (
    login,
    create_book,
    create_sub_collection,
    create_section,
)


def test_ordering_on_collection_create(client):
    login(client)
    book = create_book(client)

    root_collection = m.Collection.query.filter_by(is_root=True).first()
    assert root_collection
    assert root_collection.is_root

    for position in range(0, 10):
        collection, _ = create_sub_collection(client, book.id, root_collection.id)
        assert collection.position == position


def test_change_collection_ordering(client):
    login(client)
    book = create_book(client)

    root_collection = m.Collection.query.filter_by(is_root=True).first()
    assert root_collection
    assert root_collection.is_root

    current_ordering = {}  # collection_id : position
    for position in range(0, 10):
        collection, _ = create_sub_collection(client, book.id, root_collection.id)
        assert collection.position == position
        current_ordering[collection.id] = collection.position

    collection: m.Collection = db.session.get(m.Collection, 3)
    new_position = 4
    assert current_ordering[collection.id] != new_position
    response: Response = client.post(
        f"/book/{book.id}/{collection.id}/collection/change_position",
        headers={"Content-Type": "application/json"},
        json=dict(
            position=new_position,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200
    collection: m.Collection = db.session.get(m.Collection, 3)
    assert current_ordering[collection.id] != collection.position
    assert collection.position == new_position
    for collection in m.Collection.query.filter_by(parent_id=root_collection.id).all():
        if collection.position < new_position:
            assert current_ordering[collection.id] == collection.position
        elif collection.position > new_position:
            assert current_ordering[collection.id] + 1 == collection.position


def test_ordering_on_section_create(client):
    login(client)
    book = create_book(client)

    root_collection = m.Collection.query.filter_by(is_root=True).first()
    assert root_collection
    assert root_collection.is_root

    for position in range(0, 10):
        section, _ = create_section(client, book.id, root_collection.id)
        assert section.position == position


def test_change_section_ordering(client):
    login(client)
    book = create_book(client)

    root_collection = m.Collection.query.filter_by(is_root=True).first()
    assert root_collection
    assert root_collection.is_root
    collection_1, _ = create_sub_collection(client, book.id, root_collection.id)
    collection_2, _ = create_sub_collection(client, book.id, root_collection.id)

    current_ordering = {}  # collection_id : position
    for position in range(0, 10):
        section, _ = create_section(client, book.id, collection_1.id)
        assert section.position == position
        current_ordering[section.id] = section.position

    section: m.Section = db.session.get(m.Section, 3)
    new_position = 4
    assert current_ordering[section.id] != new_position
    response: Response = client.post(
        f"/book/{book.id}/{section.id}/section/change_position",
        headers={"Content-Type": "application/json"},
        json=dict(position=new_position),
        follow_redirects=True,
    )

    assert response.status_code == 200
    section: m.Section = db.session.get(m.Section, 3)
    assert current_ordering[section.id] != section.position
    assert section.position == new_position
    for section in m.Section.query.filter_by(collection_id=collection_1.id).all():
        if section.position < new_position:
            assert current_ordering[section.id] == section.position
        elif section.position > new_position:
            assert current_ordering[section.id] + 1 == section.position

    new_position = 999
    assert section.collection_id == collection_1.id
    assert not len(collection_2.active_sections)
    response: Response = client.post(
        f"/book/{book.id}/{section.id}/section/change_position",
        headers={"Content-Type": "application/json"},
        json=dict(position=new_position, collection_id=collection_2.id),
        follow_redirects=True,
    )
    assert response.status_code == 200

    section: m.Section = db.session.get(m.Section, section.id)
    assert section.collection_id != collection_1.id
    assert section.collection_id == collection_2.id

    collection: m.Collection = section.collection
    assert len(collection.active_sections) == 1
    assert section.position != new_position
    assert section.position == 1

    response: Response = client.post(
        f"/book/{book.id}/{section.id}/section/change_position",
        headers={"Content-Type": "application/json"},
        json=dict(position=new_position, collection_id=999),
        follow_redirects=True,
    )
    assert response.status_code == 404
    assert response.json["message"] == "collection not found"
