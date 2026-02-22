# api/routers/disciplines.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.api.schemas import DisciplineRead, ProgramSummary
from src.db.models import Discipline, Program

router = APIRouter(
    prefix="/disciplines",
    tags=["disciplines"]
)

@router.get("/", response_model=list[DisciplineRead])
def list_disciplines(db: Session = Depends(get_db)):
    """Return all disciplines."""
    return db.query(Discipline).all()


@router.get("/{discipline_id}", response_model=DisciplineRead)
def get_discipline(discipline_id: int, db: Session = Depends(get_db)):
    """Return a single discipline by ID."""
    discipline = (
        db.query(Discipline)
        .filter(Discipline.discipline_id == discipline_id)
        .first()
    )
    if not discipline:
        raise HTTPException(status_code=404, detail="Discipline not found")
    return discipline


@router.get("/{discipline_id}/programs", response_model=list[ProgramSummary])
def get_programs_by_discipline(discipline_id: int, db: Session = Depends(get_db)):
    """
    Return all programs associated with a discipline.
    Uses the simplified ProgramSummary schema.
    """
    programs = (
        db.query(
            Program.program_stream_id,
            Program.program_name,
            Program.program_url,
        )
        .filter(Program.discipline_id == discipline_id)
        .all()
    )

    return [ProgramSummary(**row._asdict()) for row in programs]