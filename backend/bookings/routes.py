from typing import Annotated
from db.models import User as UserDB, Time_slot_status, Time_slot, Booking
from users.security import get_current_active_user, authenticate_user, create_access_token, get_password_hash
from schemas import UserResponse, Token, UserCreate
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from fastapi import Depends, APIRouter, HTTPException, status
from db.db import get_session
from users.users import read_user_by_id, require_admin, read_users, update_user_profile_by_id, change_user_password, change_user_role, delete_user_by_id, deactivate_user_by_id, activate_user_by_id
from schemas import TimeSlotSchema, BookingSchema, TimeSlotCreate, BookingCreate
from users.schemas import UserResponse
from bookings.bookings import create_time_slot, update_time_slot, read_time_slots, delete_time_slot, create_booking, read_bookings, update_booking, get_booking_by_id, delete_booking, read_bookings_by_professional
from datetime import datetime
from decimal import Decimal

router = APIRouter(
    prefix="/servicios",
    tags=["servicios"]
)

@router.get("/horarios", response_model=list[TimeSlotSchema])
async def read_time_slots_from_db(db: Annotated[Session, Depends(get_session)],
                                   
) -> list[TimeSlotSchema]:
    
    slot = read_time_slots(db=db)
    
    return slot

@router.get("/reservas", response_model=list[BookingSchema])
async def read_bookings_by_prof(db: Annotated[Session, Depends(get_session)],
                                current_user: Annotated[UserDB, Depends(require_admin)],
                                   
) -> list[BookingSchema]:
    
    booking = read_bookings_by_professional(db=db,
                                            prof_user_id=current_user.user_id)
    
    return booking

@router.get("/reservas/{booking_id}", response_model=BookingSchema)
async def read_booking_by_id(db: Annotated[Session, Depends(get_session)],
                                booking_id: int,
                                current_user: Annotated[UserDB, Depends(require_admin)],                                   
) -> BookingSchema:
    
    booking = get_booking_by_id(db=db,
                                booking_id=booking_id)
    
    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    
    if booking.prof_user_id  != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a esta reserva"
        )
    
    return booking

@router.post("/horarios/nuevo-horario", response_model=TimeSlotSchema)
async def create_new_time_slot(db: Annotated[Session, Depends(get_session)],
                               slot_data: TimeSlotCreate,
                               current_user: Annotated[UserDB, Depends(require_admin)], 
                                                  
) -> TimeSlotSchema:
    
    slot = create_time_slot(db=db,
                               prof_user_id=current_user.user_id, 
                               start_at=slot_data.start_at,
                               end_at=slot_data.end_at,
                               capacity=slot_data.capacity,
                               status=slot_data.status,
                               price=slot_data.price)
    
    return slot

@router.post("/reservas/nueva-reserva", response_model=BookingSchema)
async def create_new_booking(db: Annotated[Session, Depends(get_session)],
                             booking_data: BookingCreate,
                             current_user: Annotated[UserDB, Depends(get_current_active_user)], 
                                  
) -> BookingSchema:
    
    time_slot = db.get(Time_slot, booking_data.time_slot_id)
    
    if time_slot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Horario no encontrado"
        )
    
    booking = create_booking(db=db,
                             user_id=current_user.user_id,
                             time_slot_id=time_slot.time_slot_id)
    
    return booking

@router.patch("/horarios/{time_slot_id}/actualizar-horario", response_model=TimeSlotSchema)
async def update_time_slot_at_db(db: Annotated[Session, Depends(get_session)],
                                 time_slot_id: int,
                                 slot_data: TimeSlotCreate,
                                 current_user: Annotated[UserDB, Depends(require_admin)], 
                                                  
) -> TimeSlotSchema:
    
    slot = db.get(Time_slot, time_slot_id)

    if slot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Horario no encontrado"
        )
    
    if slot.prof_user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para modificar este horario"
        )
    
    slot = update_time_slot(db=db,
                            time_slot_id=time_slot_id,
                            start_at=slot_data.start_at,
                            end_at=slot_data.end_at,
                            capacity=slot_data.capacity,
                            status=slot_data.status,
                            price=slot_data.price)
    
    return slot

@router.patch("/reservas/{booking_id}/actualizar-reserva", response_model=BookingSchema)
async def update_booking_at_db(db: Annotated[Session, Depends(get_session)],
                               booking_id: int,
                               booking_data: BookingCreate,
                               current_user: Annotated[UserDB, Depends(get_current_active_user)], 
                                  
) -> BookingSchema:
    
    booking = get_booking_by_id(
        db=db,
        booking_id=booking_id
    )    
    
    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
        
    if booking.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para modificar esta reserva"
        )
        
    new_time_slot = db.get(Time_slot, booking_data.time_slot_id)

    if new_time_slot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Horario no encontrado"
        )
    
    booking = update_booking(db=db,
                             time_slot_id=booking_data.time_slot_id,
                             booking_id=booking_id)
    
    return booking

@router.delete("/horarios/{time_slot_id}", response_model=TimeSlotSchema)
async def delete_time_slot_at_db(db: Annotated[Session, Depends(get_session)],
                           current_user: Annotated[UserDB, Depends(require_admin)], 
                           time_slot_id: int
                                                  
) -> TimeSlotSchema:
    
    slot = db.get(Time_slot, time_slot_id)

    if slot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Horario no encontrado"
        )

    if slot.prof_user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar este horario"
        )
    
    return delete_time_slot(db=db,
                            user_id=current_user.user_id, 
                            time_slot_id=time_slot_id)
    

@router.delete("/reservas/{booking_id}", response_model=BookingSchema)
async def delete_booking_at_db(db: Annotated[Session, Depends(get_session)],
                             current_user: Annotated[UserDB, Depends(get_current_active_user)], 
                             booking_id: int
                                  
) -> BookingSchema:
    
    booking = db.get(Booking, booking_id)

    
    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )

    if booking.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para eliminar esta reserva"
        )
    
    return delete_booking(db=db,
                          booking_id=booking_id,
                          actor_user_id=current_user.user_id)
    

