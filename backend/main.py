from fastapi import FastAPI
from sqlmodel import SQLModel, Session, select

from db.db import engine
from admin.auditlog import get_audit_log
from db.models import User, Booking, Time_slot

app = FastAPI()
SQLModel.metadata.create_all(engine)

@app.get("/")
def root():
    return {"message": "FastAPI funcionando"}

@app.get("/users")
def get_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users
    
@app.get("/bookings")
def get_bookings():
    with Session(engine) as session:
        bookings = session.exec(select(Booking)).all()
        return bookings

@app.get("/audit-log")
def get_all_audit_logs():
    return get_audit_log()

@app.get("/time-slots")
def get_timeslots():
    with Session(engine) as session:
        timeslots = session.exec(select(Time_slot)).all()
        return timeslots