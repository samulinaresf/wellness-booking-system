from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum

class User_role(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"

class User(SQLModel, table=True):
    user_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    phone_number: str | None = None
    role: User_role = Field(default=User_role.USER)
    profile_pic: str | None = None
    bio: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    last_login_at: datetime | None = None

class Time_slot_status(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"

class Time_slot(SQLModel, table=True):
    time_slot_id: int | None = Field(default=None, primary_key=True)
    prof_user_id: int | None = Field(default=None, foreign_key="user.user_id")
    start_at: datetime = Field(default_factory=datetime.utcnow)
    end_at: datetime = Field(default_factory=datetime.utcnow)
    capacity: int
    status: Time_slot_status = Field(default=Time_slot_status.AVAILABLE)

class Booking(SQLModel, table=True):
    booking_id: int | None = Field(default=None, primary_key=True)
    time_slot_id: int | None = Field(default=None, foreign_key="time_slot.time_slot_id")
    prof_user_id: int | None = Field(default=None, foreign_key="user.user_id")
    user_id: int | None = Field(default=None, foreign_key="user.user_id")
    price: float
    
class Audit_log(SQLModel, table=True):
    audit_log_id: int | None = Field(default=None, primary_key=True)
    booking_id: int | None = Field(default=None, foreign_key="booking.booking_id")
    user_id: int | None = Field(default=None, foreign_key="user.user_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata_details: str | None = None
    