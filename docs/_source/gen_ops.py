"""Generate 03_Operation_Manual.docx for the PMO Service."""
import os
import docstyle as ds

OUT = os.path.join(os.path.dirname(__file__), "..", "03_Operation_Manual.docx")
VER, DATE = "v1.1", "6 August 2026"

doc = ds.new_doc()
ds.footer(doc, "OFFICIAL-SENSITIVE", VER)
ds.title_page(doc, "DOC-03", "Operation Manual", "Running, deploying & maintaining the PMO Service",
              VER, DATE, "Douglas Colvin, P3MAI", "OFFICIAL-SENSITIVE")
ds.doc_control(doc, [
    ["v1.0", "2026-08-01", "Douglas Colvin", "Initial issue"],
    [VER, "2026-08-06", "Douglas Colvin", "Front-door move: served at apps.p3mai.com/pmo (APP_BASE=/pmo/), legacy app.p3mai.com 301s; CI + Dependabot; optional Sentry"],
])
ds.add_toc(doc)

ds.heading(doc, "1.  Purpose & audience", 1)
ds.para(doc, "For whoever runs and maintains the **PMO Service** — locally and on Render. Covers "
        "configuration, data, deployment, monitoring, backup, security and troubleshooting. "
        "Architecture is in **DOC-01**; usage in **DOC-02**.")

ds.heading(doc, "2.  System summary", 1)
ds.table(doc, ["Item", "Value"], [
    ["What", "Single-origin web app: FastAPI backend serving a React SPA, SQLite database"],
    ["Repository", "github.com/DRC63/pmo-service (private)"],
    ["Production", "Render Docker web service"],
    ["URL", "apps.p3mai.com/pmo (behind the apps front door; origin pmo-service.onrender.com)"],
    ["Database", "SQLite (pmo.db), auto-seeded on boot; ephemeral"],
    ["Dev ports", "backend 8000, frontend 5173"],
    ["Auth", "None in v1 (open) — flag before sensitive data"],
], col_widths=[3.4, 12.1])

ds.heading(doc, "3.  Configuration", 1)
ds.para(doc, "Environment variables (a local `.env` in `backend/` is read automatically; in production "
        "set them in the Render dashboard).")
ds.table(doc, ["Variable", "Default", "Purpose"], [
    ["DATABASE_URL", "sqlite:///…/pmo.db", "SQLAlchemy URL; point at Postgres to persist"],
    ["CORS_ORIGINS", "http://localhost:5173", "Allowed origins in split local dev"],
    ["PORT", "8000", "Set by Render automatically; the container binds to it"],
    ["APP_BASE", "/pmo/ (build arg)", "SPA base path for the front door; local dev builds use /"],
    ["SENTRY_DSN", "(unset)", "Set in Render to activate error tracking; inert otherwise"],
], col_widths=[3.4, 4.6, 7.5])

ds.heading(doc, "4.  Running locally", 1)
ds.para(doc, "Dev servers are registered in the working-directory `.claude/launch.json` as "
        "`pmo-service-backend` (8000) and `pmo-service-frontend` (5173).")
ds.heading(doc, "4.1  Backend", 2)
ds.code_block(doc, "cd backend\npython -m venv venv\n.\\venv\\Scripts\\Activate.ps1\n"
                   "pip install -r requirements.txt\npython -m app.seed\n"
                   "uvicorn app.main:app --reload --port 8000")
ds.para(doc, "API docs: http://localhost:8000/docs.")
ds.heading(doc, "4.2  Front end", 2)
ds.code_block(doc, "cd frontend\nnpm install\nnpm run dev")
ds.para(doc, "Runs at http://localhost:5173, proxying `/api/*` to the backend on 8000.")

ds.heading(doc, "5.  Data management", 1)
ds.para(doc, "On boot, if there are no projects, the app seeds a sample portfolio. To wipe and reload:")
ds.code_block(doc, "cd backend\npython -m app.seed --force")
ds.callout(doc, "pitfall", "Schema changes need a fresh DB",
           ["SQLAlchemy's create_all makes missing tables but won't add new columns to an existing "
            "table. After a model change, delete the DB then reseed:",
            "`del backend\\pmo.db*`  then  `python -m app.seed --force`"])

ds.heading(doc, "6.  Deployment", 1)
ds.para(doc, "Deployed on Render as a Docker web service built from the multi-stage `Dockerfile` "
        "(Node stage builds the React bundle; Python stage runs uvicorn and serves it). The database "
        "re-seeds on boot, so a fresh container comes up populated.")
ds.heading(doc, "6.1  Deploying a change", 2)
ds.para(doc, "Commit and push to `main`; if auto-deploy is enabled on the Render service it rebuilds "
        "automatically, otherwise trigger a manual deploy in the Render dashboard. CI (pytest + "
        "vitest) runs on every push; enable Render's wait-for-CI setting (ENG-13) to make a red "
        "build block the deploy. Dependabot raises weekly dependency PRs.")
ds.code_block(doc, "git add -A\ngit commit -m \"...\"\ngit push origin main")
ds.heading(doc, "6.2  Rollback", 2)
ds.para(doc, "In the Render dashboard, open the service → **Events**, find the previous good deploy and "
        "**Redeploy**; or revert the commit and push.")

ds.heading(doc, "7.  Monitoring & health", 1)
ds.bullet(doc, "**Health probe** — `GET /api/health` returns `{\"status\":\"ok\"}`.")
ds.bullet(doc, "**Logs / metrics** — Render dashboard → the service → **Logs** (live tail) and **Metrics**.")
ds.bullet(doc, "**Cold start** — on a free instance the service sleeps after inactivity (~50s wake); a "
          "plain 404 right after deploy is routing propagation — retry shortly.")

ds.heading(doc, "8.  Backup & persistence", 1)
ds.para(doc, "Because the database re-seeds from code on every boot, the **repository is the source of "
        "truth** and the running DB is disposable. Any real data entered in the app is **not durable** "
        "on the current ephemeral disk. To keep data, attach a Render persistent disk (point "
        "`DATABASE_URL` at a file on it) or migrate to Postgres.")
ds.callout(doc, "pitfall", "Data is not durable yet",
           ["On the current hosting, anything entered in the running app is lost on the next "
            "redeploy/restart. Do not use it as a system of record until persistence is added."])

ds.heading(doc, "9.  Website integration", 1)
ds.para(doc, "The P3MAI website's Services page (PMO card) has an **Example** button to this app, and "
        "the app's sidebar has a **Back to Website** link. Both are env-aware (`localhost` in dev, the "
        "real domain in production) so nothing needs editing between environments.")

ds.heading(doc, "10.  Security operations", 1)
ds.bullet(doc, "**No authentication in v1** — the app is open at apps.p3mai.com/pmo by deliberate choice.")
ds.bullet(doc, "**Do not store sensitive data** until authentication is added.")
ds.bullet(doc, "This manual is OFFICIAL-SENSITIVE because it details deployment and the open posture.")

ds.heading(doc, "11.  Troubleshooting", 1)
ds.table(doc, ["Symptom", "Likely cause", "Fix"], [
    ["Data reverted after deploy", "Ephemeral disk re-seeded", "Expected; add persistence for durable data"],
    ["App slow on first hit", "Instance woke from sleep", "Wait; consider a paid instance"],
    ["Graph/screen won't load", "Old cache / JS error", "Hard-refresh; check console; confirm /api/health returns ok"],
    ["New column missing after model change", "create_all won't alter tables", "Delete the DB and reseed (§5)"],
    ["Build fails on Render", "Dependency / Dockerfile issue", "Read the build log; reproduce with docker build locally"],
], col_widths=[4.4, 4.1, 7.0])

ds.heading(doc, "12.  Routine runbooks", 1)
ds.heading(doc, "12.1  Reseed / refresh sample data", 2)
ds.para(doc, "Locally: `python -m app.seed --force`. In production the DB re-seeds automatically on the "
        "next deploy/restart.")
ds.heading(doc, "12.2  Deploy a change", 2)
ds.para(doc, "Commit, push to main, and confirm the new build goes live in the Render dashboard; check "
        "app.p3mai.com and /api/health.")

ds.heading(doc, "Appendix A — API routers", 1)
ds.table(doc, ["Router", "Resource"], [
    ["projects, milestones", "Portfolio and its checkpoints"],
    ["resources, allocations", "People and their assignment to projects"],
    ["risks", "The risk register"],
    ["dashboard, reports", "Aggregated views (read-only)"],
], col_widths=[4.5, 11.0])

doc.save(OUT)
print("wrote", os.path.basename(OUT), os.path.getsize(OUT), "bytes")
