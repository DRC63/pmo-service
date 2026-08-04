# PMO Service — project notes for Claude

A lightweight PMO tool: projects, milestones, resources/allocations, risks, and a
dashboard. Part of the P3MAI suite (same stack as `../method-map`, `../p3m3-assessment`).
**Live at `apps.p3mai.com/pmo`** behind the shared front door (`../apps-gateway`).
Read `README.md` for the full picture; this file is the quick orientation.

## Stack & ports
- Backend: FastAPI + SQLAlchemy + SQLite (`pmo.db`), WAL + synchronous=NORMAL.
- Frontend: React 19 + Vite.
- Dev ports: backend **8000**, frontend **5173** (in the working-dir `.claude/launch.json`
  as `pmo-service-backend` / `pmo-service-frontend`). Method-map uses 8002/5175, p3m3
  8001/5174 — don't collide.

## Data model (`app/models.py`)
`Project` → `Milestone`, `Resource` → `Allocation` (a resource assigned to a project),
`Risk`. Routers mirror these: `projects`, `milestones`, `resources`, `allocations`,
`risks`, plus `dashboard` (aggregates) and `reports` (exports). Auto-seeds demo data on
an empty DB at boot.

## Auth — none (deliberate)
No authentication: single-user tool, deployed fully open (Douglas's call for v1). There
is no `security.py`. Revisit if it ever holds real, non-demo data (see the portfolio
backlog ENG-03).

## Deployment
- **Docker on Render**, a single service (`pmo-service`, `pmo-service.onrender.com`).
  **No `render.yaml`** (not Blueprint-managed) — `APP_BASE=/pmo/` is baked as the
  **Dockerfile default** so the SPA builds for the `/pmo` base; local dev builds at `/`.
- Served behind the front door at `apps.p3mai.com/pmo`. `main.py` has a middleware that
  **301-redirects the legacy `app.p3mai.com/*` → `apps.p3mai.com/pmo/*`** (deep path
  preserved), so that old domain didn't need moving.
- Render disk is **ephemeral** → auto-seeds on boot; authoring edits don't survive a
  redeploy (add a persistent disk / Postgres if they must — portfolio backlog ENG-02).
- Push to `main` auto-deploys.

## CI, dependencies, error tracking
- `.github/workflows/ci.yml` runs backend pytest + frontend vitest on push/PR (Python
  3.12 / Node 20); `dependabot.yml` raises weekly update PRs.
- `app/observability.py` → `init_sentry("pmo-service")` is **inert unless `SENTRY_DSN`
  is set** (lazy import; no-op locally and in tests).

## Tests
- Backend: `pytest` (isolated per-test SQLite DB). Frontend: `npm test` (Vitest).
- Verify with the repo venv: `backend/venv/Scripts/python.exe -m pytest -q`.

## Gotchas
- Project tree is under OneDrive → expect a ~2s SQLite write-commit tax that pragmas
  can't remove (sync driver). WAL keeps reads snappy.
- The cross-link to the website uses runtime host detection, not hardcoded URLs — don't
  "fix" the localhost defaults to production URLs (breaks local dev).
