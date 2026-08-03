"""Pydantic request/response schemas — the API contract.

Each resource typically has a Base (shared fields), Create/Update variants (what a
client may send) and an Out variant (what the API returns, including enriched
fields such as owner_name that aren't stored columns). Keeping these separate from
the ORM models lets the wire format evolve independently of the database and gives
FastAPI its automatic request validation and generated docs.
"""
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from .enums import MilestoneStatus, ProjectCategory, RagStatus, RiskStatus


# ---------- Resource ----------
class ResourceBase(BaseModel):
    name: str
    role: str | None = None
    email: str | None = None
    weekly_capacity_hours: float = 40
    active: bool = True


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    name: str | None = None
    role: str | None = None
    email: str | None = None
    weekly_capacity_hours: float | None = None
    active: bool | None = None


class ResourceOut(ResourceBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------- Allocation ----------
class AllocationBase(BaseModel):
    resource_id: int
    project_id: int
    allocation_pct: float = 0
    start_date: date | None = None
    end_date: date | None = None


class AllocationCreate(AllocationBase):
    pass


class AllocationUpdate(BaseModel):
    allocation_pct: float | None = None
    start_date: date | None = None
    end_date: date | None = None


class AllocationOut(AllocationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    resource_name: str | None = None
    project_name: str | None = None


class ResourceDetailOut(ResourceOut):
    allocations: list[AllocationOut] = []


# ---------- Milestone ----------
class MilestoneBase(BaseModel):
    name: str
    due_date: date | None = None
    status: MilestoneStatus = MilestoneStatus.NOT_STARTED
    sort_order: int = 0
    notes: str | None = None


class MilestoneCreate(MilestoneBase):
    pass


class MilestoneUpdate(BaseModel):
    name: str | None = None
    due_date: date | None = None
    status: MilestoneStatus | None = None
    sort_order: int | None = None
    notes: str | None = None


class MilestoneOut(MilestoneBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    project_id: int
    is_overdue: bool = False


# ---------- Risk ----------
class RiskBase(BaseModel):
    title: str
    description: str | None = None
    likelihood: int
    impact: int
    status: RiskStatus = RiskStatus.OPEN
    mitigation_plan: str | None = None
    owner_resource_id: int | None = None


class RiskCreate(RiskBase):
    project_id: int


class RiskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    likelihood: int | None = None
    impact: int | None = None
    status: RiskStatus | None = None
    mitigation_plan: str | None = None
    owner_resource_id: int | None = None


class RiskOut(RiskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    project_id: int
    score: int
    created_at: datetime
    updated_at: datetime
    project_name: str | None = None
    owner_name: str | None = None


# ---------- Project ----------
class ProjectBase(BaseModel):
    name: str
    code: str
    category: ProjectCategory = ProjectCategory.OTHER
    owner_resource_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    budget: float | None = None
    actual_spend: float = 0
    rag_status: RagStatus = RagStatus.GREEN
    description: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    category: ProjectCategory | None = None
    owner_resource_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    budget: float | None = None
    actual_spend: float | None = None
    rag_status: RagStatus | None = None
    description: str | None = None


class ProjectOut(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
    owner_name: str | None = None


class ProjectDetailOut(ProjectOut):
    milestones: list[MilestoneOut] = []
    risks: list[RiskOut] = []
    allocations: list[AllocationOut] = []


# ---------- Dashboard ----------
class UpcomingMilestoneOut(BaseModel):
    project_id: int
    project_name: str
    milestone_id: int
    name: str
    due_date: date | None
    days_until: int | None


class HighSeverityRiskOut(BaseModel):
    risk_id: int
    project_id: int
    project_name: str
    title: str
    score: int
    status: RiskStatus


class DashboardSummary(BaseModel):
    rag_counts: dict[str, int]
    total_projects: int
    upcoming_milestones: list[UpcomingMilestoneOut]
    high_severity_risks: list[HighSeverityRiskOut]
    overdue_milestones_count: int


# ---------- Reports ----------
class PortfolioRow(BaseModel):
    project_id: int
    name: str
    code: str
    category: ProjectCategory
    rag_status: RagStatus
    owner_name: str | None
    pct_milestones_complete: float
    open_risk_count: int
    top_risk_score: int
    budget: float | None
    actual_spend: float


class ProjectReport(BaseModel):
    project: ProjectDetailOut
    pct_milestones_complete: float
    open_risk_count: int
    top_risk_score: int
