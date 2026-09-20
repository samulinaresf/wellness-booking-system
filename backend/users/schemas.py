#schemas.py

from db.models import User_role
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str 
    
class UserResponse(BaseModel):
    name: str
    email: EmailStr
    role: User_role
    is_active: bool
    email_verified: bool
    
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_number: str | None = None
    profile_pic: str | None = None
    bio: str | None = None
    
class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    phone_number: str | None = None
    profile_pic: str | None = None
    bio: str | None = None
    
class ChangePassword(BaseModel):
    current_password: str
    new_password: str
    
class MessageResponse(BaseModel):
    message: str