"""
Database engine and session factory for SQLModel/SQLAlchemy.
Used by FastAPI (get_db) and by ETL scripts.
"""
from sqlmodel import create_engine, Session
from src.config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)


def SessionLocal():
    """Return a new SQLModel session (used by FastAPI dependency)."""
    return Session(engine)


def get_session():
    """Context manager for ETL or scripts: yield a session and close after use."""
    with Session(engine) as session:
        yield session