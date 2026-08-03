"""Database engine, session factory and the FastAPI DB dependency.

SQLite by default (a local pmo.db file); set DATABASE_URL to a Postgres URL to make
the data durable in production. check_same_thread=False is required because FastAPI
handles requests across a thread pool, and SQLite otherwise refuses to reuse a
connection from a different thread.
"""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DATABASE_URL = f"sqlite:///{os.path.join(BACKEND_DIR, 'pmo.db')}"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Per-request database session, used as a FastAPI dependency. The session is
# yielded to the request handler and always closed afterwards — even if the handler
# raises — so connections are never leaked.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
