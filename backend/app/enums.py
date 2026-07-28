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


HIGH_SEVERITY_RISK_THRESHOLD = 15
