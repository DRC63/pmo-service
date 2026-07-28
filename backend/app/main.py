import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .routers import allocations, dashboard, milestones, projects, reports, resources, risks

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PMO Service API")

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router)
app.include_router(milestones.router)
app.include_router(resources.router)
app.include_router(allocations.router)
app.include_router(risks.router)
app.include_router(dashboard.router)
app.include_router(reports.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


# In production, this backend also serves the built React frontend (npm run
# build in frontend/) so the whole app lives behind one origin. Locally,
# frontend/dist won't exist (the frontend runs via its own Vite dev server
# instead), so this block is skipped and dev workflow is unaffected.
FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"

if FRONTEND_DIST.is_dir():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        candidate = FRONTEND_DIST / full_path
        if full_path and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(FRONTEND_DIST / "index.html")
