import httpx
import json
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.weather import WeatherReading, Alert
import redis.asyncio as redis

class WeatherService:
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = settings.OPENWEATHER_BASE_URL
        
    async def fetch_weather_data(self, city: str) -> Dict[str, Any]:
        """Fetch weather data from OpenWeatherMap API"""
        async with httpx.AsyncClient() as client:
            # Current weather
            weather_url = f"{self.base_url}/weather"
            weather_params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            }
            
            # Air quality
            aqi_url = f"{self.base_url}/air_pollution"
            
            weather_response = await client.get(weather_url, params=weather_params)
            weather_data = weather_response.json()
            
            # Get coordinates for AQI
            lat, lon = weather_data["coord"]["lat"], weather_data["coord"]["lon"]
            aqi_params = {"lat": lat, "lon": lon, "appid": self.api_key}
            
            aqi_response = await client.get(aqi_url, params=aqi_params)
            aqi_data = aqi_response.json()
            
            return {
                "city": city,
                "temperature": weather_data["main"]["temp"],
                "humidity": weather_data["main"]["humidity"],
                "pressure": weather_data["main"]["pressure"],
                "aqi": aqi_data["list"][0]["main"]["aqi"],
                "weather_condition": weather_data["weather"][0]["main"]
            }
    
    def save_weather_reading(self, db: Session, weather_data: Dict[str, Any]) -> WeatherReading:
        """Save weather reading to database"""
        reading = WeatherReading(**weather_data)
        db.add(reading)
        db.commit()
        db.refresh(reading)
        return reading
    
    async def check_thresholds_and_alert(self, db: Session, reading: WeatherReading, redis_client):
        """Check if weather data breaches thresholds and send alerts"""
        alerts = []
        
        # Temperature alerts
        if reading.temperature > settings.TEMP_HIGH_THRESHOLD:
            alert = self._create_alert(
                db, "temperature", settings.TEMP_HIGH_THRESHOLD, 
                reading.temperature, reading.city,
                f"High temperature alert: {reading.temperature}°C in {reading.city}"
            )
            alerts.append(alert)
            
        elif reading.temperature < settings.TEMP_LOW_THRESHOLD:
            alert = self._create_alert(
                db, "temperature", settings.TEMP_LOW_THRESHOLD,
                reading.temperature, reading.city,
                f"Low temperature alert: {reading.temperature}°C in {reading.city}"
            )
            alerts.append(alert)
        
        # Humidity alerts
        if reading.humidity > settings.HUMIDITY_HIGH_THRESHOLD:
            alert = self._create_alert(
                db, "humidity", settings.HUMIDITY_HIGH_THRESHOLD,
                reading.humidity, reading.city,
                f"High humidity alert: {reading.humidity}% in {reading.city}"
            )
            alerts.append(alert)
        
        # AQI alerts
        if reading.aqi and reading.aqi > settings.AQI_HIGH_THRESHOLD:
            alert = self._create_alert(
                db, "aqi", settings.AQI_HIGH_THRESHOLD,
                reading.aqi, reading.city,
                f"Poor air quality alert: AQI {reading.aqi} in {reading.city}"
            )
            alerts.append(alert)
        
        # Publish alerts to Redis for WebSocket broadcasting
        for alert in alerts:
            alert_data = {
                "id": alert.id,
                "type": alert.alert_type,
                "message": alert.message,
                "city": alert.city,
                "timestamp": alert.created_at.isoformat()
            }
            await redis_client.publish("weather_alerts", json.dumps(alert_data))
        
        return alerts
    
    def _create_alert(self, db: Session, alert_type: str, threshold: float, 
                     actual: float, city: str, message: str) -> Alert:
        """Create and save alert to database"""
        alert = Alert(
            alert_type=alert_type,
            threshold_value=threshold,
            actual_value=actual,
            city=city,
            message=message
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert