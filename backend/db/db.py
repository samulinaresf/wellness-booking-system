from sqlmodel import create_engine, Session, select
import os

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL no está configurada")

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session