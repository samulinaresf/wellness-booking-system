from sqlmodel import create_engine, Session, delete
import os
import pytest
from dotenv import load_dotenv
from db.models import User, Time_slot, Booking, Audit_log, PasswordChangeRequest

load_dotenv()

DATABASE_TEST_URL = os.getenv("DATABASE_TEST_URL")

if not DATABASE_TEST_URL:
    raise RuntimeError("DATABASE_TEST_URL no está configurada")

engine = create_engine(DATABASE_TEST_URL)

@pytest.fixture
def test_session():
    with Session(engine) as session:
        try:
            yield session
            
        finally:
            session.rollback()
            session.exec(delete(Audit_log))
            session.exec(delete(Booking))
            session.exec(delete(Time_slot))
            session.exec(delete(PasswordChangeRequest))
            session.exec(delete(User))
            session.commit()