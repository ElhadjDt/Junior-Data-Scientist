from typing import List
import os

from dotenv import load_dotenv
from sqlmodel import Session, select
from src.db.session import engine
from src.db.models import ProgramDocument

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


FAISS_PATH = "../data/embeddings/faiss_index"


load_dotenv()
# Verify key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set in the environment or .env file.")


# ---------------------------------------------------------
# Load documents from PostgreSQL
# ---------------------------------------------------------
def load_documents() -> List[dict]:
    """
    Loads all ProgramDocument entries from the database.
    Returns a list of dicts with id, section_name, and content.
    """
    with Session(engine) as session:
        stmt = select(ProgramDocument)
        rows = session.exec(stmt).all()

    documents = []
    for row in rows:
        documents.append(
            {
                "id": row.id,
                "program_id": row.program_id,
                "section_name": row.section_name,
                "content": row.content,
            }
        )

    print(f"Loaded {len(documents)} documents from ProgramDocument.")
    return documents


# ---------------------------------------------------------
# Chunking (split long text into smaller pieces)
# ---------------------------------------------------------
def chunk_documents(documents: List[dict]):
    """
    Splits each document into smaller chunks using a text splitter.
    Returns a list of LangChain Document objects.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    chunks = []
    for doc in documents:
        sub_docs = splitter.create_documents(
            texts=[doc["content"]],
            metadatas=[
                {
                    "program_id": doc["program_id"],
                    "section_name": doc["section_name"],
                    "source_id": doc["id"],
                }
            ],
        )
        chunks.extend(sub_docs)

    print(f"Created {len(chunks)} text chunks.")
    return chunks


# ---------------------------------------------------------
# Build FAISS vector store
# ---------------------------------------------------------
def build_vectorstore(chunks, persist_path: str = FAISS_PATH):
    """
    Builds a FAISS vector store from text chunks and saves it locally.
    """
    # OpenAIEmbeddings utilisera OPENAI_API_KEY depuis l'environnement
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"  # par exemple, modèle pas cher
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(persist_path)

    print(f"FAISS vector store saved to: {persist_path}")
    return vectorstore


# ---------------------------------------------------------
# Load FAISS vector store
# ---------------------------------------------------------
def load_vectorstore(persist_path: str = FAISS_PATH):
    """
    Loads an existing FAISS vector store from disk.
    """
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vectorstore = FAISS.load_local(
        persist_path,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    print(f"FAISS vector store loaded from: {persist_path}")
    return vectorstore


# ---------------------------------------------------------
# Full pipeline (optional)
# ---------------------------------------------------------
def build_embeddings_pipeline(csv_loaded: bool = True):
    """
    Full pipeline:
    - load documents from DB
    - chunk them
    - build and save FAISS index
    """
    documents = load_documents()
    chunks = chunk_documents(documents)
    build_vectorstore(chunks)


if __name__ == "__main__":
    build_embeddings_pipeline()
