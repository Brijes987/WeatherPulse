from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.weather import WeatherReading
from app.services.weather_service import WeatherService
from pydantic import BaseModel

router = APIRouter()
weather_service = WeatherService()

class WeatherResponse(BaseModel):
    id: int
    city: str
    temperature: float
    humidity: float
    pressure: float
    aqi: Optional[int]
    weather_condition: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

@router.get("/current/{city}", response_model=WeatherResponse)
async def get_current_weather(city: str, db: Session = Depends(get_db)):
    """Get current weather for a city"""
    try:
        weather_data = await weather_service.fetch_weather_data(city)
        reading = weather_service.save_weather_reading(db, weather_data)
        return reading
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch weather data: {str(e)}")

@router.get("/history/{city}", response_model=List[WeatherResponse])
async def get_weather_history(
    city: str,
    db: Session = Depends(get_db),
    hours: int = Query(24, description="Number of hours to look back"),
    limit: int = Query(100, description="Maximum number of records")
):
    """Get weather history for a city"""
    since = datetime.utcnow() - timedelta(hours=hours)
    
    readings = db.query(WeatherReading).filter(
        WeatherReading.city == city,
        WeatherReading.timestamp >= since
    ).order_by(desc(WeatherReading.timestamp)).limit(limit).all()
    
    return readings

@router.get("/latest", response_model=List[WeatherResponse])
async def get_latest_readings(
    db: Session = Depends(get_db),
    limit: int = Query(10, description="Number of latest readings")
):
    """Get latest weather readings across all cities"""
    readings = db.query(WeatherReading).order_by(
        desc(WeatherReading.timestamp)
    ).limit(limit).all()
    
    return readings