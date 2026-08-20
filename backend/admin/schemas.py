from pydantic import BaseModel
from datetime import datetime
from db.models import User_role

class AuditLogResponse(BaseModel):
    booking_id: int | None
    user_id: int | None
    created_at: datetime
    metadata_details: str | None
    
class UserEoleUpdate(BaseModel):
    role: User_role | None = None