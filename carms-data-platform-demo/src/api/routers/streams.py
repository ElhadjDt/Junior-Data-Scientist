# src/api/routers/streams.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import distinct

from src.api.deps import get_db
from src.api.schemas import StreamName
from src.db.models import Stream

router = APIRouter(
    prefix="/streams",
    tags=["streams"]
)


@router.get("/", response_model=list[StreamName])
def list_streams(db: Session = Depends(get_db)):
    """
    Return only the unique program_stream values.
    No IDs, no programs.
    """
    rows = db.query(distinct(Stream.program_stream)).all()
    return [StreamName(program_stream=row[0]) for row in rows]