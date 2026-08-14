from db.models import User, User_role, Time_slot, Time_slot_status, Booking
from sqlmodel import Session, select
from datetime import datetime
from admin.auditlog import register_metadata_in_audit_log

def create_time_slot(db: Session,
                     prof_user_id: int,
                     start_at: datetime,
                     end_at: datetime,
                     capacity: int,
                     status: Time_slot_status):
    
    time_slot = Time_slot(prof_user_id=prof_user_id, start_at=start_at, end_at=end_at, capacity=capacity, status=status)
    
    db.add(time_slot)
    db.commit()
    db.refresh(time_slot)
    
    register_metadata_in_audit_log(db=db,
                                   booking_id=None,
                                   user_id=prof_user_id,
                                   created_at=datetime.now(),
                                   metadata_details=f"Nueva reserva disponible con el profesional {prof_user_id} de {start_at} a {end_at}")
    
    
def update_time_slot(db: Session,
                     time_slot_id: int,
                     prof_user_id: int,
                     start_at: datetime,
                     end_at: datetime,
                     capacity: int,
                     status: Time_slot_status):
    
    time_slot = db.get(Time_slot, time_slot_id)
    
    if time_slot is None:
        return None
    
    if prof_user_id is not None:
        time_slot.prof_user_id = prof_user_id
    
    if start_at is not None:
        time_slot.start_at = start_at
        
    if end_at is not None:
        time_slot.end_at = end_at
    
    if capacity is not None:
        time_slot.capacity = capacity
    
    if status is not None:
        time_slot.status = status
    
    db.add(time_slot)
    db.commit()
    db.refresh(time_slot)
        
    register_metadata_in_audit_log(db=db,
                                   booking_id=None,
                                   user_id=prof_user_id,
                                   created_at=datetime.now(),
                                   metadata_details=f"Slot de reserva {time_slot_id} actualizado.")
    
def read_time_slots():
    None

def delete_time_slot():
    None

def create_booking():
    None

def read_bookings():
    None

def get_booking_by_id():
    None

def update_booking():
    None

def cancel_booking():
    None

def delete_booking():
    None


"""

class Booking(SQLModel, table=True):
    booking_id: int | None = Field(default=None, primary_key=True)
    time_slot_id: int | None = Field(default=None, foreign_key="time_slot.time_slot_id")
    prof_user_id: int | None = Field(default=None, foreign_key="user.user_id")
    user_id: int | None = Field(default=None, foreign_key="user.user_id")
    price: float
    
"""