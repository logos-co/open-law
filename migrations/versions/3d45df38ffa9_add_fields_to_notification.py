"""add_fields_to_notification

Revision ID: 3d45df38ffa9
Revises: 8f9233babba4
Create Date: 2023-06-09 17:23:32.809580

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3d45df38ffa9"
down_revision = "8f9233babba4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    action = postgresql.ENUM(
        "CREATE",
        "EDIT",
        "DELETE",
        "VOTE",
        "APPROVE",
        "CONTRIBUTING",
        "MENTION",
        name="actions",
    )
    action.create(op.get_bind())

    entity = postgresql.ENUM(
        "SECTION",
        "COLLECTION",
        "INTERPRETATION",
        "COMMENT",
        "BOOK",
        name="entities",
    )
    entity.create(op.get_bind())
    with op.batch_alter_table("notifications", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "action",
                sa.Enum(
                    "CREATE",
                    "EDIT",
                    "DELETE",
                    "VOTE",
                    "APPROVE",
                    "CONTRIBUTING",
                    "MENTION",
                    name="actions",
                ),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "entity",
                sa.Enum(
                    "SECTION",
                    "COLLECTION",
                    "INTERPRETATION",
                    "COMMENT",
                    "BOOK",
                    name="entities",
                ),
                nullable=True,
            )
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    action = postgresql.ENUM(
        "CREATE",
        "EDIT",
        "DELETE",
        "VOTE",
        "APPROVE",
        "CONTRIBUTING",
        "MENTION",
        name="actions",
    )
    action.drop(op.get_bind())

    entity = postgresql.ENUM(
        "SECTION",
        "COLLECTION",
        "INTERPRETATION",
        "COMMENT",
        "BOOK",
        name="entities",
    )
    entity.drop(op.get_bind())
    with op.batch_alter_table("notifications", schema=None) as batch_op:
        batch_op.drop_column("entity")
        batch_op.drop_column("action")

    # ### end Alembic commands ###
