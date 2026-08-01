"""Generate the three PowerPoint summary decks for the PMO Service docs."""
import os
from deckstyle import Deck, NAVY

DOCS = os.path.join(os.path.dirname(__file__), "..")
A = lambda n: os.path.join(DOCS, "assets", n)

# 01 Architecture
d = Deck("DOC-01", "OFFICIAL")
d.title_slide("Architecture & Design", "Technical design of the P3MAI PMO Service — summary")
d.bullets("What it is", [
    "Internal PMO tool for P3MAI.",
    "Projects, milestones, resources, allocations, risks — plus dashboard & reports.",
    "Single-origin web app; SQLite auto-seeds a sample portfolio.",
], lead="One place to run a delivery portfolio.")
d.table("Technology stack", ["Layer", "Technology"], [
    ["Backend", "FastAPI + SQLAlchemy + SQLite"],
    ["Front end", "React 19 + Vite, react-router"],
    ["Packaging", "Docker (multi-stage), single image"],
    ["Hosting", "Render — Docker web service (app.p3mai.com)"],
], col_widths=[3.5, 8.6])
d.image("Deployment architecture", A("pmo_deployment.png"),
        lead="One container serves the API and the built React app.")
d.image("Data model", A("pmo_datamodel.png"),
        lead="Project → Milestones/Risks/Allocations; Resource via Allocation.")
d.image("The screens", A("pmo_screens.png"),
        lead="Dashboard, Projects, Resources, Risks, Reports (+ Settings).")
d.bullets("Backend", [
    "REST routers per resource; explicit serializers add computed fields.",
    "Dashboard aggregates RAG, upcoming milestones, high-severity risks, overdue.",
    "Reports: portfolio table + per-project drill-down.",
])
d.bullets("Security & deployment", [
    ("No authentication in v1 — open by deliberate choice (single-user).", NAVY),
    "Deployed on Render from the Dockerfile; DB re-seeds on boot.",
    "Ephemeral disk — entered data is not durable yet.",
])
d.table("Key design decisions", ["Decision", "Why"], [
    ["Single-origin Docker image", "One container serves API + UI"],
    ["SQLite + auto-seed", "Zero-config; self-populating"],
    ["No auth in v1", "Frictionless single-user tool (revisit)"],
    ["Explicit serializers", "Deliberate computed fields (RAG, overdue, %)"],
], col_widths=[5.0, 7.1])
d.bullets("Roadmap", [
    "Authentication and multi-user before real data.",
    "Persistent storage (disk / Postgres).",
    "Richer reporting and export.",
])
d.save(os.path.join(DOCS, "01_Architecture_and_Design_Summary.pptx"))

# 02 User
d = Deck("DOC-02", "OFFICIAL")
d.title_slide("User Manual", "Using the P3MAI PMO Service — summary")
d.bullets("What the PMO Service does", [
    "Track projects, milestones, resources, allocations and risks.",
    "See portfolio health on a dashboard and in reports.",
    "Pre-loaded with a sample portfolio to explore.",
])
d.image("The screens", A("pmo_screens.png"), lead="A sidebar switches between screens.")
d.bullets("Dashboard", [
    "RAG counts across the portfolio.",
    "Upcoming milestones with days remaining.",
    "High-severity risks (score 15+).",
    "Overdue-milestone count.",
])
d.bullets("Projects", [
    "Filterable portfolio list; create/edit projects.",
    "Project detail brings milestones, risks and allocations together.",
    "Budget vs. spend and percent-complete per project.",
])
d.bullets("Resources & allocations", [
    "People with role, email and weekly capacity.",
    "Allocation = % of a person on a project.",
    "Over-allocation is shown so you can rebalance.",
])
d.bullets("Risks", [
    "Register scored by likelihood × impact (1–25).",
    "15+ is high severity and shows on the dashboard.",
    "Set status (Open / Mitigating / Closed), owner, mitigation.",
])
d.table("Reading the colours", ["Indicator", "Meaning"], [
    ["Green / Amber / Red", "Project health (on track / at risk / in trouble)"],
    ["Risk-score badge", "likelihood × impact — higher & redder = more severe"],
    ["Overdue flag", "Milestone past its due date, not complete"],
], col_widths=[3.8, 8.3])
d.bullets("Good to know", [
    "No login in v1 — don't store sensitive data yet.",
    "'Back to Website' returns you to p3mai.com.",
    "Sample data can be edited or deleted freely.",
])
d.save(os.path.join(DOCS, "02_User_Manual_Summary.pptx"))

# 03 Ops
d = Deck("DOC-03", "OFFICIAL-SENSITIVE")
d.title_slide("Operation Manual", "Running, deploying & maintaining the PMO Service — summary")
d.table("System at a glance", ["Item", "Value"], [
    ["Repository", "github.com/DRC63/pmo-service (private)"],
    ["Production", "Render Docker web service"],
    ["URL", "app.p3mai.com (pmo-service.onrender.com)"],
    ["Database", "SQLite, auto-seeded on boot; ephemeral"],
    ["Dev ports", "backend 8000 · frontend 5173"],
], col_widths=[3.2, 8.9])
d.table("Configuration (env vars)", ["Variable", "Purpose"], [
    ["DATABASE_URL", "SQLAlchemy URL; point at Postgres to persist"],
    ["CORS_ORIGINS", "Allowed origins in split local dev"],
    ["PORT", "Set by Render automatically"],
], col_widths=[3.6, 8.5])
d.bullets("Running locally", [
    "Backend: venv → pip install → python -m app.seed → uvicorn …:app --port 8000.",
    "Front end: npm install → npm run dev (port 5173).",
    "Registered in .claude/launch.json.",
])
d.bullets("Data & deployment", [
    "Auto-seeds a sample portfolio when the DB is empty; reseed with --force.",
    "After a schema change, delete the DB then reseed.",
    "Deployed on Render from the Dockerfile; DB re-seeds on boot.",
    "Ephemeral disk — entered data is not durable yet.",
])
d.bullets("Monitoring & health", [
    "Health probe: GET /api/health → {status: ok}.",
    "Render dashboard → Logs (live tail) and Metrics.",
    "A plain 404 right after deploy is routing propagation — retry shortly.",
])
d.bullets("Backup & persistence", [
    "The repo (seed code) is the source of truth; the DB is disposable.",
    "For durable data: attach a Render disk or migrate to Postgres.",
])
d.table("Troubleshooting (top items)", ["Symptom", "Fix"], [
    ["Data reverted after deploy", "Expected — add persistence for durable data"],
    ["New column missing", "Delete DB and reseed"],
    ["Slow first hit", "Instance woke from sleep — wait"],
    ["Build fails on Render", "Read the build log; reproduce with docker build"],
], col_widths=[4.6, 7.5])
d.bullets("Security", [
    "No authentication in v1 — open by deliberate choice.",
    "Do not store sensitive data until auth is added.",
])
d.save(os.path.join(DOCS, "03_Operation_Manual_Summary.pptx"))
print("done — PMO decks")
