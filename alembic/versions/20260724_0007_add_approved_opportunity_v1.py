"""Add approved_opportunity_v1 table.

Revision ID: 20260724_0007
Revises: 20260720_0006
"""
from alembic import op
import sqlalchemy as sa

revision = "20260724_0007"
down_revision = "20260720_0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("review_decisions", sa.Column("created_by", sa.String(length=255), nullable=True))

    op.create_table(
        "approved_opportunities_v1",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("stable_id", sa.String(length=36), nullable=False),
        sa.Column("schema_version", sa.String(length=50), nullable=False),
        sa.Column("conversation_id", sa.Integer(), nullable=False),
        sa.Column("assessment_id", sa.Integer(), nullable=False),
        sa.Column("presumptive_candidate_id", sa.Integer(), nullable=False),
        sa.Column("public_actor_id", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=False),
        sa.Column("public_username", sa.String(length=255), nullable=True),
        sa.Column("apparent_affinity", sa.String(length=30), nullable=False),
        sa.Column("apparent_intention", sa.String(length=40), nullable=False),
        sa.Column("evidence_fragments", sa.JSON(), nullable=False),
        sa.Column("review_priority", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("human_review_id", sa.Integer(), nullable=False),
        sa.Column("human_reviewer_identity", sa.String(length=255), nullable=False),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="READY_FOR_CRM"),
        sa.Column("external_crm_id", sa.String(length=255), nullable=True),
        sa.Column("export_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_exported_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"]),
        sa.ForeignKeyConstraint(["assessment_id"], ["conversation_assessments_v3.id"]),
        sa.ForeignKeyConstraint(["presumptive_candidate_id"], ["presumptive_candidates.id"]),
        sa.ForeignKeyConstraint(["public_actor_id"], ["public_actors.id"]),
        sa.ForeignKeyConstraint(["human_review_id"], ["review_decisions.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("human_review_id", name="uq_opportunity_human_review"),
    )
    op.create_index("ix_approved_opportunities_v1_stable_id", "approved_opportunities_v1", ["stable_id"])
    op.create_index("ix_approved_opportunities_v1_conversation_id", "approved_opportunities_v1", ["conversation_id"])
    op.create_index("ix_approved_opportunities_v1_public_actor_id", "approved_opportunities_v1", ["public_actor_id"])
    op.create_index("ix_approved_opportunities_v1_status", "approved_opportunities_v1", ["status"])


def downgrade() -> None:
    op.drop_index("ix_approved_opportunities_v1_status", table_name="approved_opportunities_v1")
    op.drop_index("ix_approved_opportunities_v1_public_actor_id", table_name="approved_opportunities_v1")
    op.drop_index("ix_approved_opportunities_v1_conversation_id", table_name="approved_opportunities_v1")
    op.drop_index("ix_approved_opportunities_v1_stable_id", table_name="approved_opportunities_v1")
    op.drop_table("approved_opportunities_v1")
    op.drop_column("review_decisions", "created_by")