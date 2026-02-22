# src/db/session.py

from sqlmodel import SQLModel, create_engine, Session
from src.config import settings

# Database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
)

# Session factory for FastAPI
def SessionLocal():
    """Return a new SQLModel session."""
    return Session(engine)

# Optional: generator for ETL or scripts
def get_session():
    """Yield a session (useful for scripts)."""
    with Session(engine) as session:
        yield session