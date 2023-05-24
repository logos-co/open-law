from app.controllers.init_access_groups import create_moderator_group
from app import models as m


def test_init_moderator_group(client):
    create_moderator_group()

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

    create_moderator_group()
    groups: list[m.AccessGroup] = m.AccessGroup.query.filter_by(name="moderator").all()
    assert len(groups) == 2
