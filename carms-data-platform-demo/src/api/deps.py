from sqlalchemy.orm import Session
from src.db.session import SessionLocal

def get_db():
    """Provide a database session."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()