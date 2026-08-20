from typing import Annotated
from db.models import User as UserDB
from security import get_current_active_user, authenticate_user, create_access_token, get_password_hash
from schemas import UserResponse, Token, UserCreate, UserUpdate, ChangePassword, MessageResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from fastapi import Depends, APIRouter, HTTPException, status
from db.db import get_session
from users import create_user, update_user_profile_by_id, change_user_password

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)


@router.get("/mi-cuenta/", response_model=UserResponse)
async def get_user_account(
    current_user: Annotated[UserDB, Depends(get_current_active_user)],
) -> UserResponse:
    return current_user

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_session)],
) -> Token:

    email = form_data.username

    user = authenticate_user(
        db,
        email,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return Token(
        access_token=access_token,
        token_type="bearer"
    )

@router.post("/", response_model=UserResponse)
async def create_user_in_db(
    user_data: UserCreate,
    db: Annotated[Session, Depends(get_session)],
) -> UserResponse:
    
    user = create_user(db=db,
                       name=user_data.name,
                       email=user_data.email,
                       password_hash=get_password_hash(user_data.password),
                       phone_number=user_data.phone_number,
                       profile_pic=user_data.profile_pic,
                       bio=user_data.bio,
                       )
    
    return user

@router.patch("/mi-cuenta", response_model=UserResponse)
async def update_user_profile(db: Annotated[Session, Depends(get_session)],
                              user_data: UserUpdate,
                              current_user: Annotated[UserDB, Depends(get_current_active_user)],

) -> UserResponse:
        
    user = update_user_profile_by_id(
            db=db,
            user_id=current_user.user_id,
            name=user_data.name,
            email=user_data.email,
            phone_number=user_data.phone_number,
            bio=user_data.bio,
            profile_pic=user_data.profile_pic)
        
    return user

@router.patch("/mi-cuenta/cambiar-contrasena", response_model=MessageResponse)
async def change_profile_password(db: Annotated[Session, Depends(get_session)],
                                  user_data: ChangePassword,
                                  current_user: Annotated[UserDB, Depends(get_current_active_user)],

) -> MessageResponse:
    
    result = change_user_password(db=db, user_id=current_user.user_id, current_password=user_data.current_password, new_password=user_data.new_password)
    
    return result
