"""
Application configuration: database URL, data paths, and FAISS index path.
All paths can be overridden via environment variables for Docker and AWS deployments.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Project root: carms-data-platform-demo/
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Default data dir: sibling of carms-data-platform-demo (repo root/data)
_DEFAULT_DATA_DIR = _PROJECT_ROOT.parent / "data"


class Settings:
    """Centralized settings for database, data directories, and RAG vector store."""

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://carms:carms@localhost:5432/carms_db",
    )

    # Base directory for raw data, extracted files, and embeddings
    DATA_DIR: Path = Path(os.getenv("DATA_DIR", str(_DEFAULT_DATA_DIR))).resolve()
    RAW_DIR: Path = DATA_DIR / "raw"
    EXTRACTED_DIR: Path = DATA_DIR / "extracted"
    EMBEDDINGS_DIR: Path = DATA_DIR / "embeddings"
    FAISS_PATH: str = os.getenv("FAISS_PATH", str(DATA_DIR / "embeddings" / "faiss_index"))

    # ETL source file paths
    DISCIPLINE_EXCEL: str = str(RAW_DIR / "1503_discipline.xlsx")
    PROGRAM_MASTER_EXCEL: str = str(RAW_DIR / "1503_program_master.xlsx")
    PROGRAM_DESCRIPTIONS_CSV: str = str(EXTRACTED_DIR / "1503_program_descriptions_x_section.csv")


settings = Settings()
