from typing import Annotated
from db.models import User as UserDB, Audit_log as AuditLogDB
from security import get_current_active_user, authenticate_user, create_access_token, get_password_hash
from schemas import UserResponse, Token, UserCreate
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from fastapi import Depends, APIRouter, HTTPException, status
from db.db import get_session
from users.users import read_user_by_id, require_superadmin, read_users, update_user_profile_by_id, change_user_password, change_user_role, delete_user_by_id, deactivate_user_by_id
from schemas import AuditLogResponse, UserRoleUpdate
from users.schemas import UserResponse
from auditlog import get_audit_log
from bookings.bookings import create_time_slot, update_time_slot, read_time_slots, delete_time_slot, create_booking, read_bookings, update_booking, get_booking_by_id, delete_booking

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.get("/usuarios/{user_id}", response_model=UserResponse)
async def read_users_by_id_from_db(db: Annotated[Session, Depends(get_session)],
                                   user_id: int,
                                   current_user: Annotated[UserDB,Depends(require_superadmin)],
) -> UserResponse:
    
    user = read_user_by_id(db=db, user_id=user_id)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    return user

@router.get("/usuarios", response_model=list[UserResponse])
async def read_users_from_db(db: Annotated[Session, Depends(get_session)],
                             current_user: Annotated[UserDB,Depends(require_superadmin)]
                            ) -> list[UserResponse]:
    
    users = read_users(db=db)
    
    return users

@router.patch("/usuarios/{user_id}", response_model=UserResponse)
async def update_user_role(db: Annotated[Session, Depends(get_session)],
                           user_id: int,
                           user_data: UserRoleUpdate,
                           current_user: Annotated[UserDB,Depends(require_superadmin)]
                          ) -> UserResponse:
        
    user = change_user_role(
        db=db,
        user_id=user_id,
        role=user_data.role,
        )
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
        
    return user

@router.get("/auditlog", response_model=list[AuditLogResponse])
async def get_audit_log_from_db(db: Annotated[Session, Depends(get_session)],
                                current_user: Annotated[UserDB,Depends(require_superadmin)]
                                ) -> list[AuditLogResponse]:
    
    return get_audit_log(db=db)
"""

delete_user_by_id() ⇒ DELETE /usuarios/{user_id}

deactivate_user_by_id() ⇒ PATCH /usuarios/{user_id}/deactivate

get_audit_log() ⇒ GET /audit-log

create_time_slots() ⇒ POST /time-slots

update_time_slots() ⇒ PATCH /time-slots/{time_slot_id}

read_time_slots() ⇒ GET /time-slots

delete_time_slots() ⇒ DELETE /time-slots/{time_slot_id}

create_booking() ⇒ POST /reservas

read_bookings() ⇒ GET /reservas

read_booking_by_id() ⇒ GET /reservas/{booking_id}

update_booking() ⇒ PATCH /reservas/{booking_id}

delete_booking() ⇒ DELETE /reservas/{booking_id}"""
