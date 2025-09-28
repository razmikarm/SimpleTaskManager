from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "sqlite:///./task_nmanager.db"
engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
