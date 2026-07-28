import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
