from db.models import User, Time_slot, Time_slot_status, Booking
from sqlmodel import Session, select
from datetime import datetime
from admin.auditlog import register_metadata_in_audit_log
from decimal import Decimal

def create_time_slot(db: Session,
                     prof_user_id: int,
                     start_at: datetime,
                     end_at: datetime,
                     capacity: int,
                     status: Time_slot_status,
                     price: Decimal):
    
    time_slot = Time_slot(prof_user_id=prof_user_id, start_at=start_at, end_at=end_at, capacity=capacity, status=status, price=price)
    
    db.add(time_slot)
    db.commit()
    db.refresh(time_slot)
    
    register_metadata_in_audit_log(db=db,
                                   booking_id=None,
                                   user_id=time_slot.prof_user_id,
                                   metadata_details=f"Nueva reserva disponible con el profesional {prof_user_id} de {start_at} a {end_at} con el precio {price}")
    
    return time_slot
    
def update_time_slot(db: Session,
                     time_slot_id: int,
                     start_at: datetime | None = None,
                     end_at: datetime | None = None,
                     capacity: int | None = None,
                     status: Time_slot_status | None = None,
                     price: Decimal | None = None):
    
    time_slot = db.get(Time_slot, time_slot_id)
    
    if time_slot is None:
        return None
    
    if start_at is not None:
        time_slot.start_at = start_at
        
    if end_at is not None:
        time_slot.end_at = end_at
    
    if capacity is not None:
        time_slot.capacity = capacity
    
    if status is not None:
        time_slot.status = status
    
    if price is not None:
            time_slot.price = price
    
    db.add(time_slot)
    db.commit()
    db.refresh(time_slot)
        
    register_metadata_in_audit_log(db=db,
                                   booking_id=None,
                                   user_id=time_slot.prof_user_id,
                                   metadata_details=f"Slot de reserva {time_slot_id} actualizado.")
    
    return time_slot
    
def read_time_slots(db: Session):
    
    time_slots = db.exec(select(Time_slot)).all()
        
    return time_slots


def delete_time_slot(db: Session,
                     time_slot_id: int,
                     user_id: int):
    
    time_slot = db.get(Time_slot, time_slot_id)
    
    if time_slot is None:
        return None
    
    register_metadata_in_audit_log(db=db,
                                   booking_id=None,
                                   user_id=user_id,
                                   metadata_details=f"Slot de reserva {time_slot_id} eliminado.")
    
    db.delete(time_slot)
    db.commit()
    
    return time_slot

def create_booking(db: Session,
                   time_slot_id: int,
                   user_id: int):
     
    time_slot = db.get(Time_slot, time_slot_id)
    
    if time_slot is None:
        return None
    
    user = db.get(User, user_id)
    
    if user is None:
        return None

    professional = db.get(User, time_slot.prof_user_id)
    
    if professional is None:
        return None
    
    if time_slot.status != Time_slot_status.AVAILABLE:
        return None
    
    booking = Booking(time_slot_id=time_slot.time_slot_id, prof_user_id=professional.user_id, user_id=user.user_id)
    
    db.add(booking)
    db.commit()
    db.refresh(booking)
    
    register_metadata_in_audit_log(db=db,
                                   booking_id=booking.booking_id,
                                   user_id=user.user_id,
                                   metadata_details=f"Nueva reserva creada {booking.booking_id} del usuario {user.user_id} con {professional.user_id}.")
    
    return booking

def read_bookings(db: Session):
    
    bookings = db.exec(select(Booking)).all()
    
    return bookings


def get_booking_by_id(db: Session,
                      booking_id: int):
    
    booking = db.get(Booking, booking_id)
        
    return booking

def read_bookings_by_professional(
    db: Session,
    prof_user_id: int
):
    bookings = db.exec(
        select(Booking).where(
            Booking.prof_user_id == prof_user_id
        )
    ).all()

    return bookings

def update_booking(db: Session,
                   booking_id: int,
                   user_id: int | None=None,
                   time_slot_id: int | None=None,
                   ):
    
    booking = db.get(Booking, booking_id)
        
    if booking is None:
        return None
            
    if user_id is not None:
        booking.user_id = user_id
            
    if time_slot_id is not None:
        new_time_slot = db.get(Time_slot, time_slot_id)

        if new_time_slot is None:
            return None

        booking.time_slot_id = new_time_slot.time_slot_id
        booking.prof_user_id = new_time_slot.prof_user_id
        
    db.add(booking)
    db.commit()
    db.refresh(booking)
            
    register_metadata_in_audit_log(db=db,
                                   booking_id=booking_id,
                                   user_id=booking.user_id,
                                   metadata_details=f"Reserva {booking_id} actualizada.")
        
    return booking

def delete_booking(db: Session,
                   booking_id: int,
                   actor_user_id: int):
    
    booking = db.get(Booking, booking_id)
    
    
    if booking is None:
        return None
    
    register_metadata_in_audit_log(db=db,
                                   booking_id=booking_id,
                                   user_id=actor_user_id,
                                   metadata_details=f"Reserva {booking_id} eliminada por {actor_user_id}.")
    
    db.delete(booking)
    db.commit()
            
    return booking
