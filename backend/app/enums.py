"""Shared enumerations and constants used across the models, schemas and routers.

Defining the fixed value sets (project category, RAG status, milestone and risk
state) in one place keeps the database, the API contract and the business logic in
agreement instead of passing loose strings around. Each inherits from `str` so the
values serialise directly to/from JSON.
"""
import enum


class ProjectCategory(str, enum.Enum):
    AI_INFRASTRUCTURE = "ai_infrastructure"
    TRANSFORMATION = "transformation"
    BANKING = "banking"
    OTHER = "other"


class RagStatus(str, enum.Enum):
    GREEN = "green"
    AMBER = "amber"
    RED = "red"


class MilestoneStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    LATE = "late"


class RiskStatus(str, enum.Enum):
    OPEN = "open"
    MITIGATING = "mitigating"
    CLOSED = "closed"


# A risk's score is likelihood × impact (each rated 1–5, so the score is 1–25).
# At or above this value a risk counts as high-severity — used for the dashboard
# risk counts and to highlight risks in reports.
HIGH_SEVERITY_RISK_THRESHOLD = 15
