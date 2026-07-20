"""Add presumptive candidate list tables.

Revision ID: 20260720_0006
Revises: 20260720_0005
"""
from alembic import op
import sqlalchemy as sa

revision = "20260720_0006"
down_revision = "20260720_0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "public_actors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("platform", sa.String(length=50), nullable=False),
        sa.Column("platform_actor_id", sa.String(length=255), nullable=False),
        sa.Column("public_username", sa.String(length=255), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=True),
        sa.Column("public_profile_url", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("platform", "platform_actor_id", name="uq_public_actor_platform_actor"),
    )
    op.create_index("ix_public_actors_platform", "public_actors", ["platform"])

    op.create_table(
        "conversation_participants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("conversation_id", sa.Integer(), nullable=False),
        sa.Column("public_actor_id", sa.Integer(), nullable=False),
        sa.Column("platform_comment_id", sa.String(length=255), nullable=True),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="author"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"]),
        sa.ForeignKeyConstraint(["public_actor_id"], ["public_actors.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("conversation_id", "public_actor_id", name="uq_conversation_participant_actor_conversation"),
    )
    op.create_index("ix_conversation_participants_conversation_id", "conversation_participants", ["conversation_id"])
    op.create_index("ix_conversation_participants_public_actor_id", "conversation_participants", ["public_actor_id"])

    op.create_table(
        "presumptive_candidates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("public_actor_id", sa.Integer(), nullable=False),
        sa.Column("conversation_id", sa.Integer(), nullable=False),
        sa.Column("assessment_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("apparent_affinity", sa.String(length=30), nullable=False),
        sa.Column("apparent_intention", sa.String(length=40), nullable=False),
        sa.Column("false_positive_risk", sa.String(length=20), nullable=False),
        sa.Column("review_priority", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("skill_version", sa.String(length=50), nullable=False),
        sa.Column("model_name", sa.String(length=200), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["assessment_id"], ["conversation_assessments_v3.id"]),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"]),
        sa.ForeignKeyConstraint(["public_actor_id"], ["public_actors.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "public_actor_id",
            "conversation_id",
            "assessment_id",
            name="uq_presumptive_candidate_actor_conversation_assessment",
        ),
    )
    op.create_index("ix_presumptive_candidates_assessment_id", "presumptive_candidates", ["assessment_id"])
    op.create_index("ix_presumptive_candidates_conversation_id", "presumptive_candidates", ["conversation_id"])
    op.create_index("ix_presumptive_candidates_public_actor_id", "presumptive_candidates", ["public_actor_id"])
    op.create_index("ix_presumptive_candidates_status", "presumptive_candidates", ["status"])


def downgrade() -> None:
    op.drop_index("ix_presumptive_candidates_status", table_name="presumptive_candidates")
    op.drop_index("ix_presumptive_candidates_public_actor_id", table_name="presumptive_candidates")
    op.drop_index("ix_presumptive_candidates_conversation_id", table_name="presumptive_candidates")
    op.drop_index("ix_presumptive_candidates_assessment_id", table_name="presumptive_candidates")
    op.drop_table("presumptive_candidates")
    op.drop_index("ix_conversation_participants_public_actor_id", table_name="conversation_participants")
    op.drop_index("ix_conversation_participants_conversation_id", table_name="conversation_participants")
    op.drop_table("conversation_participants")
    op.drop_index("ix_public_actors_platform", table_name="public_actors")
    op.drop_table("public_actors")
