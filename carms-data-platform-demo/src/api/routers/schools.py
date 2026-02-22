# src/api/routers/schools.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.api.schemas import SchoolRead, ProgramSummary
from src.db.models import School, Program

router = APIRouter(
    prefix="/schools",
    tags=["schools"]
)

@router.get("/", response_model=list[SchoolRead])
def list_schools(db: Session = Depends(get_db)):
    """Return all schools."""
    return db.query(School).all()


@router.get("/{school_id}", response_model=SchoolRead)
def get_school(school_id: int, db: Session = Depends(get_db)):
    """Return a single school by ID."""
    school = db.query(School).filter(School.school_id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school


@router.get("/{school_id}/programs", response_model=list[ProgramSummary])
def get_school_programs(school_id: int, db: Session = Depends(get_db)):
    """Return all programs associated with a school."""
    programs = (
        db.query(
            Program.program_stream_id,
            Program.program_name,
            Program.program_url,
        )
        .filter(Program.school_id == school_id)
        .all()
    )
    
    return [ProgramSummary(**row._asdict()) for row in programs]