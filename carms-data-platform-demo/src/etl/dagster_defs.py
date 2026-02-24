# src/etl/dagster_defs.py

from dagster import asset, job, Definitions

from src.etl.extract_zip import extract_zip
from src.etl.load_disciplines_from_excel import load_disciplines
from src.etl.load_programs_from_excel import load_programs
from src.etl.load_program_documents_from_csv import load_program_documents
from src.qa.embeddings import build_embeddings_pipeline


# -----------------------------
# ASSETS — ETL
# -----------------------------

@asset
def zip_extracted():
    extract_zip()
    return "zip extracted"


@asset
def disciplines_loaded(zip_extracted):
    load_disciplines()
    return "disciplines loaded"


@asset
def programs_loaded(disciplines_loaded):
    load_programs()
    return "programs loaded"


@asset
def documents_loaded(programs_loaded):
    load_program_documents()
    return "documents loaded"


# -----------------------------
# ASSET — Embeddings / FAISS
# -----------------------------

@asset
def embeddings_built():
    """
    Build the FAISS vector index from program documents.
    Equivalent to: python -m src.qa.embeddings
    """
    build_embeddings_pipeline()
    return "embeddings built"


# -----------------------------
# JOBS
# -----------------------------

@job
def etl_job():
    """Run only the ETL pipeline (load data in db)."""
    documents_loaded()


@job
def build_embeddings_job():
    """Rebuild only the FAISS vector store."""
    embeddings_built()


# -----------------------------
# DEFINITIONS
# -----------------------------

defs = Definitions(
    assets=[
        zip_extracted,
        disciplines_loaded,
        programs_loaded,
        documents_loaded,
        embeddings_built,
    ],
    jobs=[etl_job, build_embeddings_job],
)