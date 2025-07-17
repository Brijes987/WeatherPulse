from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from fastapi.responses import Response as FastAPIResponse
import time
import psutil
import redis.asyncio as redis

# Prometheus metrics
REQUEST_COUNT = Counter(
    'weather_api_requests_total',
    'Total number of API requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'weather_api_request_duration_seconds',
    'API request duration in seconds',
    ['method', 'endpoint']
)

WEATHER_FETCH_COUNT = Counter(
    'weather_fetch_total',
    'Total number of weather data fetches',
    ['city', 'status']
)

ALERT_COUNT = Counter(
    'weather_alerts_total',
    'Total number of weather alerts generated',
    ['alert_type', 'city']
)

ACTIVE_WEBSOCKET_CONNECTIONS = Gauge(
    'weather_websocket_connections_active',
    'Number of active WebSocket connections'
)

SYSTEM_CPU_USAGE = Gauge(
    'weather_system_cpu_usage_percent',
    'System CPU usage percentage'
)

SYSTEM_MEMORY_USAGE = Gauge(
    'weather_system_memory_usage_percent',
    'System memory usage percentage'
)

REDIS_CONNECTIONS = Gauge(
    'weather_redis_connections_active',
    'Number of active Redis connections'
)

DATABASE_CONNECTIONS = Gauge(
    'weather_database_connections_active',
    'Number of active database connections'
)

class MetricsMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        start_time = time.time()
        
        # Create a custom send function to capture response
        status_code = 500
        
        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)
        
        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            # Record metrics
            duration = time.time() - start_time
            method = request.method
            path = request.url.path
            
            REQUEST_COUNT.labels(
                method=method,
                endpoint=path,
                status_code=status_code
            ).inc()
            
            REQUEST_DURATION.labels(
                method=method,
                endpoint=path
            ).observe(duration)

async def update_system_metrics():
    """Update system metrics periodically"""
    try:
        # CPU and Memory usage
        SYSTEM_CPU_USAGE.set(psutil.cpu_percent())
        SYSTEM_MEMORY_USAGE.set(psutil.virtual_memory().percent)
        
        # You can add more system metrics here
        disk_usage = psutil.disk_usage('/').percent
        
    except Exception as e:
        print(f"Error updating system metrics: {e}")

def record_weather_fetch(city: str, success: bool):
    """Record weather fetch attempt"""
    status = "success" if success else "failure"
    WEATHER_FETCH_COUNT.labels(city=city, status=status).inc()

def record_alert(alert_type: str, city: str):
    """Record alert generation"""
    ALERT_COUNT.labels(alert_type=alert_type, city=city).inc()

def update_websocket_connections(count: int):
    """Update active WebSocket connections count"""
    ACTIVE_WEBSOCKET_CONNECTIONS.set(count)

async def get_metrics():
    """Get Prometheus metrics"""
    # Update system metrics before returning
    await update_system_metrics()
    return generate_latest()