"""Generate 01_Architecture_and_Design.docx for the PMO Service."""
import os
import docstyle as ds

OUT = os.path.join(os.path.dirname(__file__), "..", "01_Architecture_and_Design.docx")
ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")
VER, DATE = "v1.0", "1 August 2026"

doc = ds.new_doc()
ds.footer(doc, "OFFICIAL", VER)
ds.title_page(doc, "DOC-01", "Architecture & Design", "Technical design of the P3MAI PMO Service",
              VER, DATE, "Douglas Colvin, P3MAI", "OFFICIAL")
ds.doc_control(doc, [[VER, "2026-08-01", "Douglas Colvin", "Initial issue"]])
ds.add_toc(doc)

ds.heading(doc, "1.  Executive summary", 1)
ds.para(doc, "The **PMO Service** is an internal project-management-office tool for P3MAI. It tracks "
        "**projects, milestones, resources, allocations and risks**, and rolls them up into a "
        "**dashboard** and **portfolio/project reports**. It is a single-origin web application — a "
        "**FastAPI** backend serving a **React** single-page front end, backed by **SQLite** that "
        "auto-seeds a realistic sample portfolio on first boot.")
ds.para(doc, "It is deployed as a Docker container on Render at **app.p3mai.com**. Version 1 has **no "
        "authentication** by deliberate choice (single-user, non-sensitive demo/working data).")

ds.heading(doc, "2.  Introduction", 1)
ds.heading(doc, "2.1  Purpose & scope", 2)
ds.para(doc, "The authoritative technical reference for the PMO Service — architecture, data model, "
        "backend and front end, and deployment. Usage is in **DOC-02**; operations in **DOC-03**.")
ds.heading(doc, "2.2  Audience", 2)
ds.para(doc, "Developers and technical reviewers familiar with Python, React and containers.")
ds.heading(doc, "2.3  Definitions", 2)
ds.table(doc, ["Term", "Meaning"], [
    ["RAG", "Red / Amber / Green health status"],
    ["Allocation", "The share (%) of a resource assigned to a project"],
    ["Risk score", "likelihood × impact (1–25); ≥ 15 is high severity"],
    ["SPA", "Single-page application — the React front end"],
], col_widths=[3.0, 12.5])

ds.heading(doc, "3.  System overview", 1)
ds.para(doc, "The PMO Service gives a delivery lead one place to see and manage a portfolio:")
ds.bullet(doc, "**Projects** with code, category, owner, dates, budget, spend and RAG status;")
ds.bullet(doc, "**Milestones** per project, with due dates and status (incl. overdue detection);")
ds.bullet(doc, "**Resources** and their **allocations** across projects (with over-allocation visible);")
ds.bullet(doc, "a **risk register** scored by likelihood × impact; and")
ds.bullet(doc, "a **dashboard** and **reports** that aggregate the portfolio.")

ds.heading(doc, "4.  Technology stack", 1)
ds.table(doc, ["Layer", "Technology", "Role"], [
    ["Backend", "FastAPI + SQLAlchemy (Python 3.12)", "REST API and SPA host"],
    ["Database", "SQLite (pmo.db)", "Persistence"],
    ["Validation", "Pydantic", "Request/response schemas"],
    ["Server", "uvicorn", "ASGI server"],
    ["Front end", "React 19 + Vite, react-router", "Single-page application"],
    ["Packaging", "Docker (multi-stage)", "Single-image build & deploy"],
    ["Hosting", "Render (Docker web service)", "Production runtime"],
], col_widths=[3.2, 5.3, 7.0])

ds.heading(doc, "5.  Solution architecture", 1)
ds.para(doc, "A **single origin**: in production the FastAPI backend serves the built React bundle from "
        "`frontend/dist` and exposes the `/api/*` routes from the same process.")
ds.figure(doc, os.path.join(ASSETS, "pmo_deployment.png"),
          "Figure 1 — Deployment architecture (single-origin Docker service on Render).")

ds.heading(doc, "6.  Data model", 1)
ds.figure(doc, os.path.join(ASSETS, "pmo_datamodel.png"),
          "Figure 2 — Data model: Project with Milestones/Risks/Allocations; Resource via Allocation.")
ds.heading(doc, "6.1  Entities", 2)
ds.table(doc, ["Entity", "Key fields"], [
    ["Project", "name, code, category, owner, start/end, budget, actual_spend, rag_status, description"],
    ["Milestone", "project, name, due_date, status, sort_order, notes"],
    ["Resource", "name, role, email, weekly_capacity_hours, active"],
    ["Allocation", "resource, project, allocation_pct, start/end (Resource↔Project join)"],
    ["Risk", "project, title, likelihood, impact, score, status, mitigation_plan, owner"],
], col_widths=[3.0, 12.5])
ds.heading(doc, "6.2  Enumerations", 2)
ds.table(doc, ["Enum", "Values"], [
    ["Project category", "ai_infrastructure · transformation · banking · other"],
    ["RAG status", "green · amber · red"],
    ["Milestone status", "not_started · in_progress · complete · late"],
    ["Risk status", "open · mitigating · closed"],
], col_widths=[4.0, 11.5])
ds.callout(doc, "tip", "Risk scoring",
           ["Risk score = likelihood × impact (each 1–5, so 1–25). A score of **15 or above** is treated "
            "as high severity and surfaced on the dashboard."])

ds.heading(doc, "7.  Backend design", 1)
ds.heading(doc, "7.1  API surface", 2)
ds.table(doc, ["Router", "Endpoints (CRUD unless noted)"], [
    ["projects", "list/create/get/update/delete projects (+ nested detail)"],
    ["milestones", "list/create/update/delete milestones per project"],
    ["resources", "list/create/get/update/delete resources"],
    ["allocations", "list/create/update/delete allocations"],
    ["risks", "list/create/update/delete risks (filter by project/status/score)"],
    ["dashboard", "GET summary — RAG counts, upcoming milestones, high-severity risks, overdue count"],
    ["reports", "GET portfolio report; GET per-project report"],
], col_widths=[3.2, 12.3])
ds.para(doc, "A `/api/health` endpoint provides a liveness probe. ORM objects are converted to Pydantic "
        "responses by explicit serializers that add computed fields (owner names, `is_overdue`, "
        "percent-complete, etc.).")
ds.heading(doc, "7.2  Dashboard & reports", 2)
ds.para(doc, "The dashboard aggregates across the portfolio: RAG counts, the next upcoming milestones "
        "with days-until, the highest-severity open risks, and an overdue-milestone count. The reports "
        "produce a portfolio table (per-project percent-complete, open-risk count, top risk, budget vs "
        "spend) and a single-project drill-down.")

ds.heading(doc, "8.  Front-end design", 1)
ds.figure(doc, os.path.join(ASSETS, "pmo_screens.png"),
          "Figure 3 — The main screens.")
ds.table(doc, ["Screen", "Purpose"], [
    ["Dashboard", "Portfolio health at a glance — RAG, upcoming milestones, top risks, overdue count."],
    ["Projects", "Filterable portfolio list; a detail page per project with milestones, risks, allocations."],
    ["Resources", "People, capacity and their allocations across projects."],
    ["Risks", "The risk register with scores and status."],
    ["Reports", "Portfolio and per-project reports."],
    ["Settings", "App settings."],
], col_widths=[3.0, 12.5])
ds.para(doc, "Shared UI: a sidebar + top-bar layout, reusable forms in modals (project, resource, risk), "
        "and status chips — RAG badges and a risk-score badge — for at-a-glance reading.")

ds.heading(doc, "9.  Seeding", 1)
ds.para(doc, "On first boot against an empty database the app seeds a realistic sample portfolio "
        "(six resources; four projects — a GPU supercomputer build, a core-banking migration, a data-"
        "governance rollout and the AI-PMO pilot — with milestones, allocations and risks). Seeding is "
        "idempotent and skipped under tests.")

ds.heading(doc, "10.  Security & access control", 1)
ds.callout(doc, "pitfall", "No authentication in v1",
           ["The app has no login and is deployed openly at app.p3mai.com — a deliberate choice for a "
            "single-user tool holding non-sensitive demo/working data. Add authentication before it "
            "holds anything sensitive."])

ds.heading(doc, "11.  Deployment architecture", 1)
ds.para(doc, "Deployed on Render as a Docker web service built from the multi-stage `Dockerfile`. The "
        "database re-seeds on every boot, so a fresh or restarted container comes up populated.")
ds.table(doc, ["Aspect", "Value"], [
    ["Repository", "github.com/DRC63/pmo-service (private)"],
    ["Platform", "Render — Docker web service"],
    ["URL", "app.p3mai.com (Render: pmo-service.onrender.com)"],
    ["Persistence", "Ephemeral disk — DB resets on redeploy; auto-seeds"],
], col_widths=[3.4, 12.1])

ds.heading(doc, "12.  Key design decisions", 1)
ds.table(doc, ["Decision", "Rationale"], [
    ["Single-origin Docker image", "One container serves API + UI; nothing else to run."],
    ["SQLite + auto-seed", "Zero-config persistence; ephemeral hosts self-populate."],
    ["No auth in v1", "Single-user, non-sensitive; keeps the tool frictionless (revisit later)."],
    ["Explicit serializers", "Computed fields (RAG, overdue, %-complete) added deliberately, not leaked from ORM."],
], col_widths=[4.6, 10.9])

ds.heading(doc, "13.  Non-functional considerations", 1)
ds.bullet(doc, "**Performance** — small dataset, client-side rendering; comfortably fast.")
ds.bullet(doc, "**Portability** — one Docker image; runs anywhere containers run.")
ds.bullet(doc, "**Extensibility** — new entities/reports slot into the router + serializer pattern.")

ds.heading(doc, "14.  Roadmap", 1)
ds.bullet(doc, "Authentication and multi-user support before holding real data.")
ds.bullet(doc, "Persistent storage (disk / Postgres) so data survives redeploys.")
ds.bullet(doc, "Richer reporting and export (PDF/Excel).")

ds.heading(doc, "Appendix A — Repository layout", 1)
ds.code_block(doc,
              "pmo-service/\n"
              "  backend/app/   FastAPI app (main, models, schemas, crud, serializers,\n"
              "                 enums, seed, database, routers/)\n"
              "  frontend/src/  React app (pages/, components/, layout/, api/, theme/)\n"
              "  Dockerfile     multi-stage build\n"
              "  docs/          this documentation set")

doc.save(OUT)
print("wrote", os.path.basename(OUT), os.path.getsize(OUT), "bytes")
