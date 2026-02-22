# src/api/routers/sites.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.api.schemas import SiteRead, ProgramSummary
from src.db.models import Site, Program

router = APIRouter(
    prefix="/sites",
    tags=["sites"]
)


@router.get("/", response_model=list[SiteRead])
def list_sites(db: Session = Depends(get_db)):
    """Return all training sites."""
    return db.query(Site).all()


@router.get("/{site_id}", response_model=SiteRead)
def get_site(site_id: int, db: Session = Depends(get_db)):
    """Return a single site by ID."""
    site = db.query(Site).filter(Site.site_id == site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site


@router.get("/{site_id}/programs", response_model=list[ProgramSummary])
def get_site_programs(site_id: int, db: Session = Depends(get_db)):
    """
    Return all programs associated with a site.
    This is a simplified view using ProgramSummary.
    """
    programs = (
        db.query(
            Program.program_stream_id,
            Program.program_name,
            Program.program_url,
        )
        .filter(Program.site_id == site_id)
        .all()
    )

    # Convert SQLAlchemy Row objects to dict for Pydantic
    return [ProgramSummary(**row._asdict()) for row in programs]