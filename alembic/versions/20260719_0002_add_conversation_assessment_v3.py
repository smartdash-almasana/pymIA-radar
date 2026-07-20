"""Add versioned conversation assessment V3 storage.

Revision ID: 20260719_0002
Revises: 20260719_0001
"""
from alembic import op
import sqlalchemy as sa

revision = "20260719_0002"
down_revision = "20260719_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "conversation_assessments_v3",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "conversation_id",
            sa.Integer(),
            sa.ForeignKey("conversations.id"),
            nullable=False,
        ),
        sa.Column("schema_version", sa.String(length=100), nullable=False),
        sa.Column("assessment_status", sa.String(length=60), nullable=False),
        sa.Column("real_topic", sa.String(length=500), nullable=True),
        sa.Column("contextual_meaning", sa.Text(), nullable=True),
        sa.Column("apparent_affinity", sa.String(length=30), nullable=True),
        sa.Column("apparent_affinity_domains", sa.JSON(), nullable=False),
        sa.Column("apparent_intention", sa.String(length=40), nullable=True),
        sa.Column("intention_summary", sa.Text(), nullable=True),
        sa.Column("evidence_fragments", sa.JSON(), nullable=False),
        sa.Column("rejected_evidence_fragments", sa.JSON(), nullable=False),
        sa.Column("contradictions", sa.JSON(), nullable=False),
        sa.Column("missing_context", sa.JSON(), nullable=False),
        sa.Column("false_positive_risk", sa.String(length=20), nullable=True),
        sa.Column("uncertainty", sa.String(length=20), nullable=True),
        sa.Column("human_review_reason", sa.Text(), nullable=True),
        sa.Column("review_priority", sa.Integer(), nullable=False),
        sa.Column("recommended_review_action", sa.String(length=30), nullable=False),
        sa.Column("semantic_engine", sa.String(length=100), nullable=False),
        sa.Column("model_name", sa.String(length=200), nullable=True),
        sa.Column("safe_error_code", sa.String(length=100), nullable=True),
        sa.Column("provisional", sa.Boolean(), nullable=False),
        sa.Column("human_review_required", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_conversation_assessments_v3_conversation_id",
        "conversation_assessments_v3",
        ["conversation_id"],
    )
    op.create_index(
        "ix_conversation_assessments_v3_assessment_status",
        "conversation_assessments_v3",
        ["assessment_status"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_conversation_assessments_v3_assessment_status",
        table_name="conversation_assessments_v3",
    )
    op.drop_index(
        "ix_conversation_assessments_v3_conversation_id",
        table_name="conversation_assessments_v3",
    )
    op.drop_table("conversation_assessments_v3")
