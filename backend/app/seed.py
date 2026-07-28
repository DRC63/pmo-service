"""Populate the database with sample PMO data. Run with `python -m app.seed`.

Idempotent: skips seeding if any projects already exist, unless --force is passed
(in which case all seeded tables are wiped and reseeded).
"""
import sys
from datetime import date, timedelta

from .database import Base, SessionLocal, engine
from .enums import MilestoneStatus, ProjectCategory, RagStatus, RiskStatus
from .models import Allocation, Milestone, Project, Resource, Risk

TODAY = date.today()


def _days(n: int) -> date:
    return TODAY + timedelta(days=n)


def wipe(db):
    db.query(Risk).delete()
    db.query(Allocation).delete()
    db.query(Milestone).delete()
    db.query(Project).delete()
    db.query(Resource).delete()
    db.commit()


def seed(db):
    resources = [
        Resource(name="Douglas Colvin", role="Delivery Lead", email="drcolvin@yahoo.com", weekly_capacity_hours=40),
        Resource(name="Priya Nair", role="Program Manager", email="priya.nair@example.com", weekly_capacity_hours=40),
        Resource(name="Marcus Ellery", role="Business Analyst", email="marcus.ellery@example.com", weekly_capacity_hours=37.5),
        Resource(name="Sofia Reyes", role="Technical Program Manager", email="sofia.reyes@example.com", weekly_capacity_hours=40),
        Resource(name="James Okafor", role="Vendor Manager", email="james.okafor@example.com", weekly_capacity_hours=35),
        Resource(name="Lena Vogt", role="Data/AI Lead", email="lena.vogt@example.com", weekly_capacity_hours=40),
    ]
    db.add_all(resources)
    db.flush()  # assign ids

    douglas, priya, marcus, sofia, james, lena = resources

    projects = [
        Project(
            name="GPU Supercomputer Build — EMEA",
            code="GPU-EMEA",
            category=ProjectCategory.AI_INFRASTRUCTURE.value,
            owner_resource_id=douglas.id,
            start_date=_days(-90),
            end_date=_days(120),
            budget=45_000_000,
            actual_spend=19_500_000,
            rag_status=RagStatus.AMBER.value,
            description="Design, procurement, and build-out of a GPU compute cluster across two EMEA data centres.",
        ),
        Project(
            name="Core Banking Platform Migration",
            code="CBP-MIG",
            category=ProjectCategory.BANKING.value,
            owner_resource_id=priya.id,
            start_date=_days(-200),
            end_date=_days(30),
            budget=12_000_000,
            actual_spend=10_800_000,
            rag_status=RagStatus.GREEN.value,
            description="Migration of core ledger and payments processing to the new platform.",
        ),
        Project(
            name="Enterprise Data Governance Rollout",
            code="EDG-ROLL",
            category=ProjectCategory.TRANSFORMATION.value,
            owner_resource_id=sofia.id,
            start_date=_days(-60),
            end_date=_days(180),
            budget=3_200_000,
            actual_spend=2_100_000,
            rag_status=RagStatus.RED.value,
            description="Enterprise-wide data classification, lineage, and governance framework rollout.",
        ),
        Project(
            name="AI PMO Tooling Pilot",
            code="AI-PMO",
            category=ProjectCategory.AI_INFRASTRUCTURE.value,
            owner_resource_id=lena.id,
            start_date=_days(-30),
            end_date=_days(60),
            budget=250_000,
            actual_spend=40_000,
            rag_status=RagStatus.GREEN.value,
            description="Pilot of agentic AI tooling to automate PMO reporting and delivery workflows.",
        ),
    ]
    db.add_all(projects)
    db.flush()

    gpu, cbp, edg, aipmo = projects

    milestones = [
        # GPU-EMEA
        Milestone(project_id=gpu.id, name="Site power/cooling design sign-off", due_date=_days(-45), status=MilestoneStatus.COMPLETE.value, sort_order=1),
        Milestone(project_id=gpu.id, name="Rack delivery — Phase 1", due_date=_days(-10), status=MilestoneStatus.LATE.value, sort_order=2, notes="Vendor shipment delayed 3 weeks."),
        Milestone(project_id=gpu.id, name="Network fabric commissioning", due_date=_days(14), status=MilestoneStatus.IN_PROGRESS.value, sort_order=3),
        Milestone(project_id=gpu.id, name="Go-live — Phase 1 cluster", due_date=_days(45), status=MilestoneStatus.NOT_STARTED.value, sort_order=4),
        # CBP-MIG
        Milestone(project_id=cbp.id, name="Ledger parallel-run complete", due_date=_days(-20), status=MilestoneStatus.COMPLETE.value, sort_order=1),
        Milestone(project_id=cbp.id, name="Payments cutover rehearsal", due_date=_days(7), status=MilestoneStatus.IN_PROGRESS.value, sort_order=2),
        Milestone(project_id=cbp.id, name="Production cutover", due_date=_days(28), status=MilestoneStatus.NOT_STARTED.value, sort_order=3),
        # EDG-ROLL
        Milestone(project_id=edg.id, name="Data classification standard approved", due_date=_days(-30), status=MilestoneStatus.COMPLETE.value, sort_order=1),
        Milestone(project_id=edg.id, name="Lineage tooling deployed — Wave 1", due_date=_days(-5), status=MilestoneStatus.LATE.value, sort_order=2, notes="Blocked on procurement of lineage tool licences."),
        Milestone(project_id=edg.id, name="Governance council chartered", due_date=_days(21), status=MilestoneStatus.NOT_STARTED.value, sort_order=3),
        # AI-PMO
        Milestone(project_id=aipmo.id, name="Requirements + design workshop", due_date=_days(-15), status=MilestoneStatus.COMPLETE.value, sort_order=1),
        Milestone(project_id=aipmo.id, name="Dashboard + reporting agent pilot", due_date=_days(10), status=MilestoneStatus.IN_PROGRESS.value, sort_order=2),
        Milestone(project_id=aipmo.id, name="Pilot review with stakeholders", due_date=_days(35), status=MilestoneStatus.NOT_STARTED.value, sort_order=3),
    ]
    db.add_all(milestones)

    allocations = [
        Allocation(resource_id=douglas.id, project_id=gpu.id, allocation_pct=60, start_date=_days(-90), end_date=_days(120)),
        Allocation(resource_id=douglas.id, project_id=aipmo.id, allocation_pct=30, start_date=_days(-30), end_date=_days(60)),
        Allocation(resource_id=priya.id, project_id=cbp.id, allocation_pct=100, start_date=_days(-200), end_date=_days(30)),
        Allocation(resource_id=marcus.id, project_id=cbp.id, allocation_pct=50, start_date=_days(-200), end_date=_days(30)),
        Allocation(resource_id=marcus.id, project_id=edg.id, allocation_pct=50, start_date=_days(-60), end_date=_days(180)),
        Allocation(resource_id=sofia.id, project_id=edg.id, allocation_pct=80, start_date=_days(-60), end_date=_days(180)),
        Allocation(resource_id=sofia.id, project_id=gpu.id, allocation_pct=40, start_date=_days(-90), end_date=_days(120)),
        # James is deliberately over-allocated to exercise the AllocationBar over-100% state
        Allocation(resource_id=james.id, project_id=gpu.id, allocation_pct=70, start_date=_days(-90), end_date=_days(120)),
        Allocation(resource_id=james.id, project_id=cbp.id, allocation_pct=50, start_date=_days(-200), end_date=_days(30)),
        Allocation(resource_id=lena.id, project_id=aipmo.id, allocation_pct=90, start_date=_days(-30), end_date=_days(60)),
    ]
    db.add_all(allocations)

    def risk(project_id, title, description, likelihood, impact, status, mitigation, owner_id):
        return Risk(
            project_id=project_id,
            title=title,
            description=description,
            likelihood=likelihood,
            impact=impact,
            score=likelihood * impact,
            status=status,
            mitigation_plan=mitigation,
            owner_resource_id=owner_id,
        )

    risks = [
        risk(gpu.id, "GPU vendor supply constraint", "Global GPU shortage could delay Phase 1 racks further.", 4, 5, RiskStatus.OPEN.value, "Dual-source from secondary vendor; expedite freight for Phase 2.", douglas.id),
        risk(gpu.id, "Data centre power capacity shortfall", "Site power upgrade may not complete before Phase 2 load-in.", 3, 4, RiskStatus.MITIGATING.value, "Engaging utility provider for expedited capacity upgrade.", sofia.id),
        risk(gpu.id, "Cooling system noise compliance", "Local noise ordinance may require additional acoustic dampening.", 2, 2, RiskStatus.CLOSED.value, "Acoustic panels installed and inspected.", sofia.id),
        risk(cbp.id, "Cutover rollback complexity", "Rollback procedure for production cutover untested at full scale.", 3, 5, RiskStatus.OPEN.value, "Full rollback rehearsal scheduled ahead of cutover.", priya.id),
        risk(cbp.id, "Regulatory sign-off delay", "Regulator review of new ledger controls may slip.", 2, 4, RiskStatus.MITIGATING.value, "Weekly touchpoints with regulator liaison.", priya.id),
        risk(edg.id, "Governance council staffing gap", "Key governance roles remain unfilled, delaying charter approval.", 4, 4, RiskStatus.OPEN.value, "Interim chairs appointed pending permanent hires.", sofia.id),
        risk(edg.id, "Lineage tool licensing delay", "Procurement of lineage tooling licences behind schedule.", 3, 3, RiskStatus.OPEN.value, "Escalated to procurement lead for expedited PO.", marcus.id),
        risk(aipmo.id, "Model output reliability", "Agentic reporting outputs need human validation before wider rollout.", 2, 3, RiskStatus.MITIGATING.value, "Human-in-the-loop review gate added to pilot workflow.", lena.id),
        risk(aipmo.id, "Stakeholder adoption risk", "PMO staff may be slow to trust automated reporting.", 2, 2, RiskStatus.OPEN.value, "Early demo sessions and feedback loop with PMO staff.", lena.id),
    ]
    db.add_all(risks)

    db.commit()


def main():
    force = "--force" in sys.argv
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(Project).count()
        if existing and not force:
            print(f"Database already has {existing} project(s) — skipping seed. Pass --force to wipe and reseed.")
            return
        if existing and force:
            print("Wiping existing data...")
            wipe(db)
        seed(db)
        print("Seed complete:")
        print(f"  Resources: {db.query(Resource).count()}")
        print(f"  Projects:  {db.query(Project).count()}")
        print(f"  Milestones:{db.query(Milestone).count()}")
        print(f"  Allocations:{db.query(Allocation).count()}")
        print(f"  Risks:     {db.query(Risk).count()}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
