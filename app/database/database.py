from sqlmodel import SQLModel, Session, create_engine
from decouple import config

database_connection_string = config("CONNECTION_URI")
engine_url = create_engine(database_connection_string)


def conn():
    SQLModel.metadata.create_all(engine_url)


def get_session():
    with Session(engine_url) as session:
        yield session


def get_session_for_bot():
    return Session(engine_url)
