from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


# ---------------------------------------------------------
# TABLE: Discipline
# ---------------------------------------------------------
class Discipline(SQLModel, table=True):
    """
    Represents a medical discipline (e.g., Anesthesiology).
    discipline_id comes directly from Excel dataset.
    """
    discipline_id: int = Field(primary_key=True)
    discipline_name: str

    programs: List["Program"] = Relationship(back_populates="discipline")


# ---------------------------------------------------------
# TABLE: School
# ---------------------------------------------------------
class School(SQLModel, table=True):
    """
    Represents a university or medical school.
    school_id comes directly from  Excel dataset.
    """
    school_id: int = Field(primary_key=True)
    school_name: str

    programs: List["Program"] = Relationship(back_populates="school")


# ---------------------------------------------------------
# TABLE: Stream
# ---------------------------------------------------------
class Stream(SQLModel, table=True):
    """
    Represents a program stream (e.g., CMG Stream for CMG).
    program_stream_id comes directly from Excel dataset.
    program_stream_name is kept even though it is derivable.
    """
    program_stream_id: int = Field(primary_key=True)
    program_stream: str
    program_stream_name: str   

    programs: List["Program"] = Relationship(back_populates="stream")


# ---------------------------------------------------------
# TABLE: Site
# ---------------------------------------------------------
class Site(SQLModel, table=True):
    """
    Represents a physical training site or location (e.g., Halifax, Québec).
    site_id is auto-generated because the Excel dataset does not provide one.
    """
    site_id: Optional[int] = Field(default=None, primary_key=True)
    site_name: str

    programs: List["Program"] = Relationship(back_populates="site")


# ---------------------------------------------------------
# TABLE: Program (central fact table)
# ---------------------------------------------------------
class Program(SQLModel, table=True):
    """
    Represents a specific residency program offered by a school,
    in a discipline, at a site, within a stream.
    program_id is auto-generated because the Excel dataset does not provide one.
    """
    program_id: Optional[int] = Field(default=None, primary_key=True)

    discipline_id: int = Field(foreign_key="discipline.discipline_id")
    school_id: int = Field(foreign_key="school.school_id")
    program_stream_id: int = Field(foreign_key="stream.program_stream_id")
    site_id: int = Field(foreign_key="site.site_id")

    program_name: str
    program_url: str

    discipline: Discipline = Relationship(back_populates="programs")
    school: School = Relationship(back_populates="programs")
    stream: Stream = Relationship(back_populates="programs")
    site: Site = Relationship(back_populates="programs")


# ---------------------------------------------------------
# TABLE: ProgramDocument (for LangChain, embeddings, QA)
# ---------------------------------------------------------
class ProgramDocument(SQLModel, table=True):
    """
    Stores the textual sections of CaRMS program descriptions.
    This table is NOT part of the normalized relational model.
    It is a DOCUMENT table used for:
      - embeddings
      - semantic search
      - retrieval-augmented generation (RAG)
      - LangChain QA pipelines

    Each row represents ONE section of ONE program description.
    Example:
        program_id = 12
        section_name = "selection_criteria"
        content = "Applicants must demonstrate..."
    """
    id: Optional[int] = Field(default=None, primary_key=True)

    # Link to normalized Program table
    program_id: int = Field(foreign_key="program.program_id")

    # Document content
    section_name: str
    content: str

    # CaRMS metadata
    program_description_id: int
    document_id: Optional[str] = None
    match_iteration_id: Optional[int] = None
    source: Optional[str] = None
