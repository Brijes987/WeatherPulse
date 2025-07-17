from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json
import redis.asyncio as redis
from app.core.database import engine, Base
from app.api import weather, alerts, auth, user_alerts
from app.core.metrics import MetricsMiddleware, get_metrics
from app.models import user  # Import user models to create tables
from app.websocket.manager import ConnectionManager
from app.core.config import settings

# Create tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.redis = redis.from_url(settings.REDIS_URL)
    app.state.connection_manager = ConnectionManager()
    yield
    # Shutdown
    await app.state.redis.close()

app = FastAPI(
    title="Weather Monitoring API",
    description="Real-time weather monitoring and alerting system",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add metrics middleware
app.add_middleware(MetricsMiddleware)

# Include routers
app.include_router(weather.router, prefix="/api/weather", tags=["weather"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(user_alerts.router, prefix="/api/user", tags=["user"])

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await app.state.connection_manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and listen for Redis messages
            pubsub = app.state.redis.pubsub()
            await pubsub.subscribe("weather_alerts")
            
            async for message in pubsub.listen():
                if message["type"] == "message":
                    alert_data = json.loads(message["data"])
                    await app.state.connection_manager.broadcast(alert_data)
    except WebSocketDisconnect:
        app.state.connection_manager.disconnect(websocket)

@app.get("/")
async def root():
    return {"message": "Weather Monitoring API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    from fastapi.responses import Response
    metrics_data = await get_metrics()
    return Response(content=metrics_data, media_type="text/plain")