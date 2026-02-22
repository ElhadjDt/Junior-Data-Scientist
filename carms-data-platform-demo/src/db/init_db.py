from sqlmodel import SQLModel
from .session import engine
from .models import *

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()