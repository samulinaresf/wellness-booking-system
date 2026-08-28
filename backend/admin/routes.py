from typing import Annotated
from db.models import User as UserDB
from schemas import UserResponse
from sqlmodel import Session
from fastapi import Depends, APIRouter, HTTPException, status
from db.db import get_session
from users.users import read_user_by_id, require_superadmin, read_users, change_user_role, delete_user_by_id, deactivate_user_by_id, activate_user_by_id
from schemas import AuditLogResponse, UserRoleUpdate, UserStatusUpdate
from users.schemas import UserResponse
from auditlog import get_audit_log

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.get("/usuarios/{user_id}", response_model=UserResponse)
async def read_users_by_id_route(db: Annotated[Session, Depends(get_session)],
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
async def read_users_route(db: Annotated[Session, Depends(get_session)],
                             current_user: Annotated[UserDB,Depends(require_superadmin)]
                            ) -> list[UserResponse]:
    
    users = read_users(db=db)
    
    return users

@router.patch("/usuarios/{user_id}/rol", response_model=UserResponse)
async def change_user_role_route(db: Annotated[Session, Depends(get_session)],
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
async def get_audit_log_route(db: Annotated[Session, Depends(get_session)],
                                current_user: Annotated[UserDB,Depends(require_superadmin)]
                                ) -> list[AuditLogResponse]:
    
    return get_audit_log(db=db)

@router.delete("/usuarios/{user_id}", response_model=UserResponse)
async def delete_user_by_id_route(db: Annotated[Session, Depends(get_session)],
                           user_id: int,
                           current_user: Annotated[UserDB,Depends(require_superadmin)]
                          ) -> UserResponse:
        
    user = delete_user_by_id(
        db=db,
        user_id=user_id,
        )
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
        
    return user

@router.patch("/usuarios/{user_id}/status", response_model=UserResponse)
async def update_user_status_route(db: Annotated[Session, Depends(get_session)],
                           user_id: int,
                           user_data: UserStatusUpdate,
                           current_user: Annotated[UserDB,Depends(require_superadmin)]
                          ) -> UserResponse:
    
    
    if user_data.is_active is False:
    
        user = deactivate_user_by_id(
            db=db,
            user_id=user_id,
            )
    elif user_data.is_active is True:
        
        user = activate_user_by_id(
            db=db,
            user_id=user_id,
            )
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
        
    return user
