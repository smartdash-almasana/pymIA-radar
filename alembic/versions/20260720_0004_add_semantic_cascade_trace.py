"""Add semantic cascade trace to V3 assessments.

Revision ID: 20260720_0004
Revises: 20260719_0003
"""
from alembic import op
import sqlalchemy as sa

revision = "20260720_0004"
down_revision = "20260719_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("conversation_assessments_v3") as batch:
        batch.add_column(sa.Column("cascade_schema_version", sa.String(length=100), nullable=True))
        batch.add_column(sa.Column("gemma_review_triggered", sa.Boolean(), nullable=False, server_default=sa.false()))
        batch.add_column(sa.Column("gemma_trigger_reasons", sa.JSON(), nullable=False, server_default="[]"))
        batch.add_column(sa.Column("gemma_review", sa.JSON(), nullable=True))
        batch.add_column(sa.Column("deterministic_resolution", sa.String(length=60), nullable=True))
        batch.add_column(sa.Column("resolution_note", sa.Text(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("conversation_assessments_v3") as batch:
        batch.drop_column("resolution_note")
        batch.drop_column("deterministic_resolution")
        batch.drop_column("gemma_review")
        batch.drop_column("gemma_trigger_reasons")
        batch.drop_column("gemma_review_triggered")
        batch.drop_column("cascade_schema_version")
