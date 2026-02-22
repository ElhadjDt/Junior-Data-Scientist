# src/etl/dagster_defs.py

from dagster import asset, job, Definitions
from src.etl.load_disciplines_from_excel import load_disciplines
from src.etl.load_programs_from_excel import load_programs
from src.etl.load_program_documents_from_csv import load_program_documents
from src.qa.embeddings import build_faiss_index


# -----------------------------
# ASSETS (ETL)
# -----------------------------

@asset
def disciplines_loaded():
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
# ASSET (Embeddings)
# -----------------------------

@asset
def embeddings_built(documents_loaded):
    build_faiss_index()
    return "embeddings built"


# -----------------------------
# JOBS
# -----------------------------

@job
def etl_job():
    embeddings_built()


@job
def embeddings_job():
    embeddings_built()


# -----------------------------
# REPOSITORY
# -----------------------------

defs = Definitions(
    assets=[disciplines_loaded, programs_loaded, documents_loaded, embeddings_built],
    jobs=[etl_job, embeddings_job],
)