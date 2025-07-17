from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    custom_alerts = relationship("CustomAlert", back_populates="user")
    user_cities = relationship("UserCity", back_populates="user")

class CustomAlert(Base):
    __tablename__ = "custom_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    city = Column(String)
    alert_type = Column(String)  # temperature_high, temperature_low, humidity, aqi
    threshold_value = Column(Float)
    is_active = Column(Boolean, default=True)
    email_enabled = Column(Boolean, default=True)
    sms_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="custom_alerts")

class UserCity(Base):
    __tablename__ = "user_cities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    city = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="user_cities")