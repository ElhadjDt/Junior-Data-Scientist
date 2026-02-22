import pandas as pd
from sqlmodel import Session, select
from src.db.models import Program, ProgramDocument
from src.db.session import engine


SECTION_COLUMNS = [
    "program_contracts",
    "general_instructions",
    "supporting_documentation_information",
    "review_process",
    "interviews",
    "selection_criteria",
    "program_highlights",
    "program_curriculum",
    "training_sites",
    "additional_information",
    "return_of_service",
    "faq",
    "summary_of_changes",
]


def load_program_documents_from_csv(filepath: str):
    """
    Loads CaRMS program descriptions from CSV, normalizes them
    (wide → long), maps them to Program via program_description_id,
    and inserts them into ProgramDocument.
    """
    print(f"Loading program descriptions from: {filepath}")
    df = pd.read_csv(filepath)

    with Session(engine) as session:
        inserted = 0
        skipped = 0

        for _, row in df.iterrows():

            stmt = select(Program).where(
                Program.program_stream_id == row["program_description_id"]
            )
            program = session.exec(stmt).first()

            if not program:
                print(f"Warning: No Program found for program_description_id={row['program_description_id']}")
                skipped += 1
                continue

            for section in SECTION_COLUMNS:
                content = row.get(section)

                if not isinstance(content, str) or content.strip() == "":
                    continue

                doc = ProgramDocument(
                    program_id=program.program_id,
                    section_name=section,
                    content=content.strip(),
                    program_description_id=row["program_description_id"],
                    document_id=row["document_id"],
                    match_iteration_id=row["match_iteration_id"],
                    source=row["source"],
                )

                session.add(doc)
                inserted += 1

        session.commit()

    print("ProgramDocument loading complete.")
    print(f"Inserted documents: {inserted}")
    print(f"Skipped (no matching Program): {skipped}")

if __name__ == "__main__":
    load_program_documents_from_csv("../data/extracted/1503_program_descriptions_x_section.csv")
