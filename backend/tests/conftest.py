from sqlmodel import create_engine, Session, select
import os
import pytest
from dotenv import load_dotenv

load_dotenv()

DATABASE_TEST_URL = os.getenv("DATABASE_TEST_URL")

if not DATABASE_TEST_URL:
    raise RuntimeError("DATABASE_TEST_URL no está configurada")

engine = create_engine(DATABASE_TEST_URL)

@pytest.fixture
def test_session():
    with Session(engine) as session:
        yield session