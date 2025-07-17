from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class WeatherReading(Base):
    __tablename__ = "weather_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    pressure = Column(Float)
    aqi = Column(Integer, nullable=True)
    weather_condition = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String)  # temperature, humidity, aqi
    threshold_value = Column(Float)
    actual_value = Column(Float)
    city = Column(String)
    message = Column(String)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)