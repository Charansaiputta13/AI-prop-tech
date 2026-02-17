from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    status = Column(String, default="open") # open, in_progress, resolved, closed
    priority = Column(String, default="medium") # low, medium, high, emergency
    
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id")) # Tenant who reported it
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=True) # Optional link to property
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", backref="tickets")
