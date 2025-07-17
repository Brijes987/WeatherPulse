import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://weather_user:weather_pass@localhost:5432/weather_monitoring")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    OPENWEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5"
    
    # Alert thresholds
    TEMP_HIGH_THRESHOLD: float = 45.0
    TEMP_LOW_THRESHOLD: float = -10.0
    HUMIDITY_HIGH_THRESHOLD: float = 90.0
    AQI_HIGH_THRESHOLD: int = 150
    
    # Email configuration
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    
    # Twilio configuration
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER: str = os.getenv("TWILIO_PHONE_NUMBER", "")
    
    class Config:
        env_file = ".env"

settings = Settings()