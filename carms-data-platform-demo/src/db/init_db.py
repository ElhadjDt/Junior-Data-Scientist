"""
Create all database tables from SQLModel metadata.
Run once after PostgreSQL is up (e.g. make init-db).
"""
from sqlmodel import SQLModel
from src.db.session import engine
from src.db import models  # noqa: F401 - register all table models with SQLModel.metadata


def create_db_and_tables() -> None:
    """Create all tables defined in src.db.models."""
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()