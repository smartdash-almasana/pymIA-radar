"""Represent the schema that existed before ConversationAssessmentV3.

Revision ID: 20260719_0001
Revises: None
"""
from alembic import op
import sqlalchemy as sa

revision = "20260719_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "conversations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("external_id", sa.String(length=255), nullable=False),
        sa.Column("conversation_url", sa.Text(), nullable=False),
        sa.Column("author_name", sa.String(length=255), nullable=True),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("context", sa.Text(), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("query_origin", sa.Text(), nullable=True),
        sa.Column("engagement", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.UniqueConstraint("source", "external_id", name="uq_source_external_id"),
    )
    op.create_index("ix_conversations_source", "conversations", ["source"])
    op.create_index("ix_conversations_status", "conversations", ["status"])

    op.create_table(
        "semantic_assessments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("relevant", sa.Boolean(), nullable=False),
        sa.Column("affinity_score", sa.Integer(), nullable=False),
        sa.Column("investment_intent", sa.Integer(), nullable=False),
        sa.Column("probable_archetype", sa.String(length=100), nullable=True),
        sa.Column("conversation_stage", sa.String(length=100), nullable=True),
        sa.Column("recommended_action", sa.String(length=100), nullable=True),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("missing_data", sa.JSON(), nullable=False),
        sa.Column("risk_flags", sa.JSON(), nullable=False),
        sa.Column("reasoning_summary", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_semantic_assessments_conversation_id", "semantic_assessments", ["conversation_id"])

    op.create_table(
        "semantic_assessments_v2",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("thematic_affinity", sa.Integer(), nullable=False),
        sa.Column("values_affinity", sa.Integer(), nullable=False),
        sa.Column("intent_score", sa.Integer(), nullable=False),
        sa.Column("declared_capacity", sa.String(length=50), nullable=False),
        sa.Column("decision_stage", sa.String(length=100), nullable=False),
        sa.Column("evidence_quality", sa.Integer(), nullable=False),
        sa.Column("false_positive_risk", sa.String(length=50), nullable=False),
        sa.Column("review_priority", sa.Integer(), nullable=False),
        sa.Column("probable_archetype", sa.String(length=100), nullable=True),
        sa.Column("archetype_confidence", sa.Integer(), nullable=True),
        sa.Column("archetype_evidence", sa.JSON(), nullable=False),
        sa.Column("positive_signals", sa.JSON(), nullable=False),
        sa.Column("negative_signals", sa.JSON(), nullable=False),
        sa.Column("objections", sa.JSON(), nullable=False),
        sa.Column("missing_information", sa.JSON(), nullable=False),
        sa.Column("evidence_fragments", sa.JSON(), nullable=False),
        sa.Column("recommended_action", sa.String(length=100), nullable=False),
        sa.Column("human_review_required", sa.Boolean(), nullable=False),
        sa.Column("provisional", sa.Boolean(), nullable=False),
        sa.Column("semantic_engine", sa.String(length=50), nullable=False),
        sa.Column("model_name", sa.String(length=200), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_semantic_assessments_v2_conversation_id", "semantic_assessments_v2", ["conversation_id"])

    op.create_table(
        "review_decisions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("decision", sa.String(length=50), nullable=False),
        sa.Column("edited_response", sa.Text(), nullable=True),
        sa.Column("reviewer_notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_review_decisions_conversation_id", "review_decisions", ["conversation_id"])

    op.create_table(
        "engagement_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("channel", sa.String(length=50), nullable=True),
        sa.Column("message_text", sa.Text(), nullable=True),
        sa.Column("response_text", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_engagement_events_conversation_id", "engagement_events", ["conversation_id"])
    op.create_index("ix_engagement_events_event_type", "engagement_events", ["event_type"])

    op.create_table(
        "qualification_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("input_payload", sa.JSON(), nullable=False),
        sa.Column("traffic_light", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("radar_state", sa.String(length=50), nullable=False),
        sa.Column("recommended_path", sa.String(length=100), nullable=False),
        sa.Column("path_requires_human_confirmation", sa.Boolean(), nullable=False),
        sa.Column("crm_transfer_allowed", sa.Boolean(), nullable=False),
        sa.Column("calendar_access_allowed", sa.Boolean(), nullable=False),
        sa.Column("reasons", sa.JSON(), nullable=False),
        sa.Column("missing_information", sa.JSON(), nullable=False),
        sa.Column("reviewer_notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_qualification_records_conversation_id", "qualification_records", ["conversation_id"])
    op.create_index("ix_qualification_records_traffic_light", "qualification_records", ["traffic_light"])
    op.create_index("ix_qualification_records_status", "qualification_records", ["status"])
    op.create_index("ix_qualification_records_radar_state", "qualification_records", ["radar_state"])


def downgrade() -> None:
    op.drop_table("qualification_records")
    op.drop_table("engagement_events")
    op.drop_table("review_decisions")
    op.drop_table("semantic_assessments_v2")
    op.drop_table("semantic_assessments")
    op.drop_table("conversations")
