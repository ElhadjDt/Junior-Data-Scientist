# src/etl/dagster_defs.py

from dagster import asset, job, Definitions

from src.etl.load_disciplines_from_excel import load_disciplines
from src.etl.load_programs_from_excel import load_programs
from src.etl.load_program_documents_from_csv import load_program_documents
from src.qa.embeddings import build_embeddings_pipeline  # equivalent to: python -m src.qa.embeddings


# -----------------------------
# ASSETS (ETL)
# -----------------------------

@asset
def disciplines_loaded():
    """Load disciplines from Excel into PostgreSQL (equivalent to part of the manual ETL pipeline)."""
    load_disciplines()
    return "disciplines loaded"


@asset
def programs_loaded(disciplines_loaded):
    """Load programs from Excel into PostgreSQL."""
    load_programs()
    return "programs loaded"


@asset
def documents_loaded(programs_loaded):
    """Load program descriptions from CSV into PostgreSQL."""
    load_program_documents()
    return "documents loaded"


# -----------------------------
# ASSET (Embeddings / FAISS)
# -----------------------------

@asset
def embeddings_built(documents_loaded):
    """
    Build the FAISS vector index from program documents.

    This asset is the Dagster equivalent of running:
        python -m src.qa.embeddings
    """
    build_embeddings_pipeline()
    return "embeddings built"


# -----------------------------
# JOBS
# -----------------------------

@job
def etl_job():
    """
    Full pipeline:
    - Load disciplines
    - Load programs
    - Load program documents
    - Build FAISS embeddings (RAG vector store)
    """
    embeddings_built()


@job
def embeddings_job():
    """
    Rebuild only the FAISS vector store (RAG embeddings),
    equivalent to re-running: python -m src.qa.embeddings
    """
    embeddings_built()


# -----------------------------
# DEFINITIONS (Dagster Repository)
# -----------------------------

defs = Definitions(
    assets=[
        disciplines_loaded,
        programs_loaded,
        documents_loaded,
        embeddings_built,
    ],
    jobs=[etl_job, embeddings_job],
)