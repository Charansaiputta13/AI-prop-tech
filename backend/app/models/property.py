from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    address = Column(String, index=True)
    city = Column(String, index=True)
    state = Column(String)
    zip_code = Column(String)
    description = Column(Text, nullable=True)
    
    units = relationship("Unit", back_populates="property")
    
class Unit(Base):
    __tablename__ = "units"
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    unit_number = Column(String)
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    rent_amount = Column(Float)
    status = Column(String, default="vacant") # vacant, occupied, maintenance
    
    property = relationship("Property", back_populates="units")
