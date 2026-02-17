from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TicketBase(BaseModel):
    title: str
    description: str
    priority: str = "medium"

class TicketCreate(TicketBase):
    pass

class Ticket(TicketBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
