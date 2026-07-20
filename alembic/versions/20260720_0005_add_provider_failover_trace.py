"""Add provider failover trace columns to V3 assessments.

Revision ID: 20260720_0005
Revises: 20260720_0004
"""
from alembic import op
import sqlalchemy as sa

revision = "20260720_0005"
down_revision = "20260720_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("conversation_assessments_v3") as batch:
        batch.add_column(sa.Column("primary_provider_attempted", sa.String(length=30), nullable=False, server_default="agnes"))
        batch.add_column(sa.Column("primary_provider_used", sa.String(length=30), nullable=True))
        batch.add_column(sa.Column("provider_failover", sa.Boolean(), nullable=False, server_default=sa.false()))
        batch.add_column(sa.Column("provider_failure_code", sa.String(length=100), nullable=True))
        batch.add_column(sa.Column("provider_failure_detail", sa.Text(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("conversation_assessments_v3") as batch:
        batch.drop_column("provider_failure_detail")
        batch.drop_column("provider_failure_code")
        batch.drop_column("provider_failover")
        batch.drop_column("primary_provider_used")
        batch.drop_column("primary_provider_attempted")
