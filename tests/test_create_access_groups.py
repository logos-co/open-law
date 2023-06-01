from app.controllers.create_access_groups import (
    create_moderator_group,
    create_editor_group,
)
from app import models as m


def test_init_moderator_group(client):
    create_moderator_group(book_id=0)

    group: m.AccessGroup = m.AccessGroup.query.filter_by(name="moderator").first()
    assert group
    assert not group.users
    assert group.permissions

    permissions = group.permissions

    access = m.Permission.Access

    interpretation_DA: m.Permission = m.Permission.query.filter_by(
        access=access.D | access.A, entity_type=m.Permission.Entity.INTERPRETATION
    ).first()
    assert interpretation_DA
    assert interpretation_DA in permissions

    comment_DA: m.Permission = m.Permission.query.filter_by(
        access=access.D | access.A, entity_type=m.Permission.Entity.COMMENT
    ).first()
    assert comment_DA
    assert comment_DA in permissions

    create_moderator_group(book_id=0)
    groups: list[m.AccessGroup] = m.AccessGroup.query.filter_by(name="moderator").all()
    assert len(groups) == 2


def test_init_editor_group(client):
    create_editor_group(book_id=0)

    group: m.AccessGroup = m.AccessGroup.query.filter_by(name="editor").first()
    assert group
    assert not group.users
    assert group.permissions

    permissions = group.permissions

    access = m.Permission.Access

    interpretation_DA: m.Permission = m.Permission.query.filter_by(
        access=access.D | access.A, entity_type=m.Permission.Entity.INTERPRETATION
    ).first()
    assert interpretation_DA
    assert interpretation_DA in permissions

    comment_DA: m.Permission = m.Permission.query.filter_by(
        access=access.D | access.A, entity_type=m.Permission.Entity.COMMENT
    ).first()
    assert comment_DA
    assert comment_DA in permissions

    section_CUD: m.Permission = m.Permission.query.filter_by(
        access=access.C | access.U | access.D,
        entity_type=m.Permission.Entity.SECTION,
    ).first()
    assert section_CUD
    assert section_CUD in permissions

    collection_CUD: m.Permission = m.Permission.query.filter_by(
        access=access.C | access.U | access.D,
        entity_type=m.Permission.Entity.COLLECTION,
    ).first()
    assert collection_CUD
    assert collection_CUD in permissions

    book_U: m.Permission = m.Permission.query.filter_by(
        access=access.U,
        entity_type=m.Permission.Entity.BOOK,
    ).first()
    assert book_U
    assert book_U in permissions

    create_editor_group(book_id=0)
    groups: list[m.AccessGroup] = m.AccessGroup.query.filter_by(name="editor").all()
    assert len(groups) == 2
