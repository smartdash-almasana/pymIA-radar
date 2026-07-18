from pydantic import BaseModel, Field

class AssessmentResult(BaseModel):
    relevant: bool
    affinity_score: int = Field(ge=0, le=100)
    investment_intent: int = Field(ge=0, le=100)
    probable_archetype: str | None = None
    conversation_stage: str | None = None
    recommended_action: str
    evidence: list[str] = Field(default_factory=list)
    missing_data: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    reasoning_summary: str
