# PMO Service

Internal PMO tool for P3MAI — projects, milestones, resources, allocations, risks, and reporting.

No authentication in v1 — single-user, localhost-only.

## Running locally

**Backend** (terminal 1):
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload --port 8000
```
API docs: http://localhost:8000/docs

**Frontend** (terminal 2):
```powershell
cd frontend
npm install
npm run dev
```
App: http://localhost:5173 (proxies `/api/*` to the backend on port 8000)

## Reseeding

`python -m app.seed` skips seeding if projects already exist. Pass `--force` to wipe and reseed:
```powershell
python -m app.seed --force
```

## Running tests

**Backend** (pytest, isolated per-test SQLite DB — never touches `pmo.db`):
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest
```

**Frontend** (Vitest + React Testing Library):
```powershell
cd frontend
npm test
```
Use `npm run test:watch` for watch mode during development.
