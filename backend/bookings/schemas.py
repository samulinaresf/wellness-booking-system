from pydantic import BaseModel
from datetime import datetime
from db.models import Time_slot_status
from decimal import Decimal

class TimeSlotSchema(BaseModel):
    prof_user_id: int
    start_at: datetime
    end_at: datetime 
    capacity: int
    status: Time_slot_status
    price: Decimal

class BookingSchema(BaseModel):
    time_slot_id: int
    prof_user_id: int
    user_id: int
    
class TimeSlotCreate(BaseModel):
    start_at: datetime
    end_at: datetime
    capacity: int
    status: Time_slot_status
    price: Decimal
    
class BookingCreate(BaseModel):
    time_slot_id: int
    
class TimeSlotUpdate(BaseModel):
    start_at: datetime | None = None
    end_at: datetime | None = None
    capacity: int | None = None
    status: Time_slot_status | None = None
    price: Decimal | None = None