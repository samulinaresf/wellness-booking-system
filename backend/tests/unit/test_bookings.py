from bookings.bookings import create_time_slot
from conftest import test_session
from datetime import datetime
from db.models import Time_slot_status
from decimal import Decimal

def test_create_time_slot(test_session):
    
    start_at = datetime(2026, 9, 1, 10, 0)
    end_at = datetime(2026, 9, 1, 11, 0)
    capacity = 3
    time_slot_status = Time_slot_status.AVAILABLE
    price = Decimal("19.65")
    
    result = create_time_slot(test_session,1,start_at=start_at,end_at=end_at,capacity=capacity,status=time_slot_status,price=price)
    
    assert result.prof_user_id == 1
    assert result.start_at == datetime(2026, 9, 1, 10, 0)
    assert result.end_at == datetime(2026, 9, 1, 11, 0)
    assert result.capacity == 3
    assert result.status == Time_slot_status.AVAILABLE
    assert result.price == Decimal("19.65")

"""#Este es el bookings.py


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
    
    if price is not None and price != time_slot.price:

        existing_booking = db.exec(
            select(Booking).where(
                Booking.time_slot_id == time_slot_id
            )
        ).first()

        if existing_booking is not None:
            raise ValueError(
                "No se puede modificar el precio de un horario con reservas"
            )

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
    
    existing_booking = db.exec(
        select(Booking).where(
            Booking.time_slot_id == time_slot_id
        )
    ).first()

    if existing_booking is not None:
        raise ValueError(
            "No se puede eliminar un horario que tiene reservas"
        )
    
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
    
    total_bookings_per_time_slot = db.exec(select(Booking).where(Booking.time_slot_id == time_slot_id)).all()
    
    if len(total_bookings_per_time_slot) >= time_slot.capacity:
        time_slot.status = Time_slot_status.UNAVAILABLE
        db.add(time_slot)
        db.commit()
        return None
    
    existing_booking = db.exec(
        select(Booking).where(
            Booking.time_slot_id == time_slot_id,
            Booking.user_id == user_id
        )
    ).first()

    if existing_booking is not None:
        return None
    
    booking = Booking(time_slot_id=time_slot.time_slot_id, prof_user_id=professional.user_id, user_id=user.user_id)
    
    db.add(booking)
    
    if len(total_bookings_per_time_slot) + 1 >= time_slot.capacity:
        time_slot.status = Time_slot_status.UNAVAILABLE
        db.add(time_slot)
    
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
                   time_slot_id: int,
                   ):
    
    booking = db.get(Booking, booking_id)
        
    if booking is None:
        return None
    
    old_time_slot = db.get(Time_slot, booking.time_slot_id)
    
    if booking.time_slot_id == time_slot_id:
        return booking
            
    new_time_slot = db.get(Time_slot, time_slot_id)

    if new_time_slot is None:
        return None
    
    if new_time_slot.status != Time_slot_status.AVAILABLE:
        return None

    existing_booking = db.exec(
        select(Booking).where(
            Booking.time_slot_id == new_time_slot.time_slot_id,
            Booking.user_id == booking.user_id
        )
    ).first()
    
    if existing_booking is not None:
        return None
    
    new_slot_bookings = db.exec(
            select(Booking).where(
                Booking.time_slot_id == new_time_slot.time_slot_id,
            )
        ).all()

    if len(new_slot_bookings) >= new_time_slot.capacity:
        return None
    
    if old_time_slot is not None:
        old_time_slot.status = Time_slot_status.AVAILABLE
        db.add(old_time_slot)
        
    booking.time_slot_id = new_time_slot.time_slot_id
    booking.prof_user_id = new_time_slot.prof_user_id
    
    if len(new_slot_bookings) + 1 >= new_time_slot.capacity:
        new_time_slot.status = Time_slot_status.UNAVAILABLE
        
    db.add(booking)
    db.add(new_time_slot)
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
    
    time_slot = db.get(
        Time_slot,
        booking.time_slot_id
    )

    if time_slot is not None:
        time_slot.status = Time_slot_status.AVAILABLE
        db.add(time_slot)
        
    register_metadata_in_audit_log(db=db,
                                   booking_id=booking_id,
                                   user_id=actor_user_id,
                                   metadata_details=f"Reserva {booking_id} eliminada por {actor_user_id}.")
    
    db.delete(booking)
    db.commit()
            
    return booking
"""