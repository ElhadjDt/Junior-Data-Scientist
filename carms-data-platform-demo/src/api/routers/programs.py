from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api.deps import get_db
from src.api.schemas import ProgramRead
from src.db.models import Program, Discipline, School, Stream, Site

router = APIRouter(
    prefix="/programs",
    tags=["programs"]
)


@router.get("/", response_model=list[ProgramRead])
def list_programs(db: Session = Depends(get_db)):
    """
    Return all programs with joined metadata:
    discipline, school, stream, site.
    """
    rows = (
        db.query(

            Discipline.discipline_id,
            Discipline.discipline_name,

            School.school_id,
            School.school_name,

            Stream.program_stream_id,
            Stream.program_stream,
            Stream.program_stream_name,

            Site.site_name.label("program_site"),

            Program.program_name,
            Program.program_url,
        )
        .join(Discipline, Program.discipline_id == Discipline.discipline_id)
        .join(School, Program.school_id == School.school_id)
        .join(Stream, Program.program_stream_id == Stream.program_stream_id)
        .join(Site, Program.site_id == Site.site_id)
        .all()
    )

    return [ProgramRead(**row._asdict()) for row in rows]


@router.get("/{program_stream_id}", response_model=list[ProgramRead])
def list_programs_by_stream(program_stream_id: int, db: Session = Depends(get_db)):
    """
    Return all programs for a given program_stream_id.
    """
    rows = (
        db.query(
            Discipline.discipline_id,
            Discipline.discipline_name,

            School.school_id,
            School.school_name,

            Stream.program_stream_id,
            Stream.program_stream,
            Stream.program_stream_name,

            Site.site_name.label("program_site"),

            Program.program_name,
            Program.program_url,
        )
        .join(Discipline, Program.discipline_id == Discipline.discipline_id)
        .join(School, Program.school_id == School.school_id)
        .join(Stream, Program.program_stream_id == Stream.program_stream_id)
        .join(Site, Program.site_id == Site.site_id)
        .filter(Stream.program_stream_id == program_stream_id)
        .all()
    )

    return [ProgramRead(**row._asdict()) for row in rows]