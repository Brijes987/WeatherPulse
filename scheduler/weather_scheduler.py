import asyncio
import os
import sys
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Add parent directory to path to import backend modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.core.database import SessionLocal
from app.services.weather_service import WeatherService
from app.core.config import settings
import redis.asyncio as redis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherScheduler:
    def __init__(self):
        self.weather_service = WeatherService()
        self.cities = [
            "New York", "London", "Tokyo", "Sydney", "Mumbai", 
            "Berlin", "Paris", "Toronto", "Singapore", "Dubai"
        ]
        self.redis_client = None
        
    async def initialize_redis(self):
        """Initialize Redis connection"""
        self.redis_client = redis.from_url(settings.REDIS_URL)
        
    async def fetch_weather_for_all_cities(self):
        """Fetch weather data for all monitored cities"""
        logger.info(f"Starting weather fetch cycle at {datetime.now()}")
        
        db = SessionLocal()
        try:
            for city in self.cities:
                try:
                    logger.info(f"Fetching weather for {city}")
                    
                    # Fetch weather data
                    weather_data = await self.weather_service.fetch_weather_data(city)
                    
                    # Save to database
                    reading = self.weather_service.save_weather_reading(db, weather_data)
                    
                    # Check thresholds and send alerts
                    alerts = await self.weather_service.check_thresholds_and_alert(
                        db, reading, self.redis_client
                    )
                    
                    if alerts:
                        logger.info(f"Generated {len(alerts)} alerts for {city}")
                    
                    logger.info(f"Successfully processed weather data for {city}")
                    
                except Exception as e:
                    logger.error(f"Error processing weather for {city}: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in weather fetch cycle: {str(e)}")
        finally:
            db.close()
            
        logger.info("Weather fetch cycle completed")

async def main():
    """Main scheduler function"""
    scheduler_instance = WeatherScheduler()
    await scheduler_instance.initialize_redis()
    
    # Create scheduler
    scheduler = AsyncIOScheduler()
    
    # Schedule weather fetching every 5 minutes
    scheduler.add_job(
        scheduler_instance.fetch_weather_for_all_cities,
        trigger=IntervalTrigger(minutes=5),
        id='weather_fetch',
        name='Fetch weather data for all cities',
        replace_existing=True
    )
    
    # Start scheduler
    scheduler.start()
    logger.info("Weather scheduler started - fetching data every 5 minutes")
    
    # Run initial fetch
    await scheduler_instance.fetch_weather_for_all_cities()
    
    try:
        # Keep the scheduler running
        while True:
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        logger.info("Shutting down scheduler...")
        scheduler.shutdown()
        await scheduler_instance.redis_client.close()

if __name__ == "__main__":
    asyncio.run(main())