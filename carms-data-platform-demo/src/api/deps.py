"""
Dependency injection: provide a database session to FastAPI route handlers.
"""
from sqlalchemy.orm import Session
from src.db.session import SessionLocal


def get_db():
    """Yield a database session; ensure it is closed after the request."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()