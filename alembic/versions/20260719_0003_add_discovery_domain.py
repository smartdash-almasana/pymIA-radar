"""Add the human discovery domain and nullable historical references.

Revision ID: 20260719_0003
Revises: 20260719_0002
"""
from alembic import op
import sqlalchemy as sa

revision = "20260719_0003"
down_revision = "20260719_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "discovery_candidates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "origin_conversation_id",
            sa.Integer(),
            sa.ForeignKey("conversations.id"),
            nullable=False,
        ),
        sa.Column("public_name", sa.String(length=255), nullable=True),
        sa.Column("public_identity_reference", sa.String(length=500), nullable=True),
        sa.Column("public_profile_url", sa.Text(), nullable=True),
        sa.Column("authorized_contact", sa.String(length=500), nullable=True),
        sa.Column("discovery_state", sa.String(length=50), nullable=False),
        sa.Column("created_by", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "origin_conversation_id",
            name="uq_discovery_candidate_origin_conversation",
        ),
    )
    op.create_index(
        "ix_discovery_candidates_origin_conversation_id",
        "discovery_candidates",
        ["origin_conversation_id"],
    )
    op.create_index(
        "ix_discovery_candidates_discovery_state",
        "discovery_candidates",
        ["discovery_state"],
    )

    op.create_table(
        "discovery_outcomes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "discovery_candidate_id",
            sa.Integer(),
            sa.ForeignKey("discovery_candidates.id"),
            nullable=False,
        ),
        sa.Column("sympathy_revealed", sa.String(length=20), nullable=False),
        sa.Column("revealed_affinity_level", sa.String(length=20), nullable=False),
        sa.Column("revealed_affinity_domains", sa.JSON(), nullable=False),
        sa.Column("motivation_declared", sa.Text(), nullable=True),
        sa.Column("questions_or_interests", sa.JSON(), nullable=False),
        sa.Column("objections", sa.JSON(), nullable=False),
        sa.Column("wants_to_continue", sa.Boolean(), nullable=False),
        sa.Column("consent_to_prequalification", sa.Boolean(), nullable=False),
        sa.Column("consent_recorded_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("human_notes", sa.Text(), nullable=True),
        sa.Column("archetype_hypothesis", sa.String(length=100), nullable=True),
        sa.Column("archetype_evidence", sa.JSON(), nullable=False),
        sa.Column("archetype_confidence", sa.Integer(), nullable=True),
        sa.Column("archetype_human_confirmed", sa.Boolean(), nullable=False),
        sa.Column("recorded_by", sa.String(length=255), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "discovery_candidate_id",
            name="uq_discovery_outcome_candidate",
        ),
    )
    op.create_index(
        "ix_discovery_outcomes_discovery_candidate_id",
        "discovery_outcomes",
        ["discovery_candidate_id"],
    )

    with op.batch_alter_table("engagement_events") as batch_op:
        batch_op.add_column(
            sa.Column("discovery_candidate_id", sa.Integer(), nullable=True)
        )
        batch_op.create_foreign_key(
            "fk_engagement_events_discovery_candidate_id",
            "discovery_candidates",
            ["discovery_candidate_id"],
            ["id"],
        )
        batch_op.create_index(
            "ix_engagement_events_discovery_candidate_id",
            ["discovery_candidate_id"],
        )

    with op.batch_alter_table("qualification_records") as batch_op:
        batch_op.add_column(
            sa.Column("discovery_candidate_id", sa.Integer(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("discovery_outcome_id", sa.Integer(), nullable=True)
        )
        batch_op.create_foreign_key(
            "fk_qualification_records_discovery_candidate_id",
            "discovery_candidates",
            ["discovery_candidate_id"],
            ["id"],
        )
        batch_op.create_foreign_key(
            "fk_qualification_records_discovery_outcome_id",
            "discovery_outcomes",
            ["discovery_outcome_id"],
            ["id"],
        )
        batch_op.create_index(
            "ix_qualification_records_discovery_candidate_id",
            ["discovery_candidate_id"],
        )
        batch_op.create_index(
            "ix_qualification_records_discovery_outcome_id",
            ["discovery_outcome_id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("qualification_records") as batch_op:
        batch_op.drop_index("ix_qualification_records_discovery_outcome_id")
        batch_op.drop_index("ix_qualification_records_discovery_candidate_id")
        batch_op.drop_constraint(
            "fk_qualification_records_discovery_outcome_id",
            type_="foreignkey",
        )
        batch_op.drop_constraint(
            "fk_qualification_records_discovery_candidate_id",
            type_="foreignkey",
        )
        batch_op.drop_column("discovery_outcome_id")
        batch_op.drop_column("discovery_candidate_id")

    with op.batch_alter_table("engagement_events") as batch_op:
        batch_op.drop_index("ix_engagement_events_discovery_candidate_id")
        batch_op.drop_constraint(
            "fk_engagement_events_discovery_candidate_id",
            type_="foreignkey",
        )
        batch_op.drop_column("discovery_candidate_id")

    op.drop_index(
        "ix_discovery_outcomes_discovery_candidate_id",
        table_name="discovery_outcomes",
    )
    op.drop_table("discovery_outcomes")

    op.drop_index(
        "ix_discovery_candidates_discovery_state",
        table_name="discovery_candidates",
    )
    op.drop_index(
        "ix_discovery_candidates_origin_conversation_id",
        table_name="discovery_candidates",
    )
    op.drop_table("discovery_candidates")
