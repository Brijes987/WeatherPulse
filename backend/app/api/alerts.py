from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.weather import Alert
from pydantic import BaseModel

router = APIRouter()

class AlertResponse(BaseModel):
    id: int
    alert_type: str
    threshold_value: float
    actual_value: float
    city: str
    message: str
    is_resolved: bool
    created_at: datetime
    resolved_at: Optional[datetime]
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[AlertResponse])
async def get_alerts(
    db: Session = Depends(get_db),
    city: Optional[str] = Query(None, description="Filter by city"),
    alert_type: Optional[str] = Query(None, description="Filter by alert type"),
    resolved: Optional[bool] = Query(None, description="Filter by resolution status"),
    hours: int = Query(24, description="Hours to look back"),
    limit: int = Query(50, description="Maximum number of alerts")
):
    """Get alerts with optional filters"""
    since = datetime.utcnow() - timedelta(hours=hours)
    
    query = db.query(Alert).filter(Alert.created_at >= since)
    
    if city:
        query = query.filter(Alert.city == city)
    if alert_type:
        query = query.filter(Alert.alert_type == alert_type)
    if resolved is not None:
        query = query.filter(Alert.is_resolved == resolved)
    
    alerts = query.order_by(desc(Alert.created_at)).limit(limit).all()
    return alerts

@router.put("/{alert_id}/resolve")
async def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    """Mark an alert as resolved"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_resolved = True
    alert.resolved_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Alert resolved successfully"}

@router.get("/stats")
async def get_alert_stats(
    db: Session = Depends(get_db),
    hours: int = Query(24, description="Hours to look back")
):
    """Get alert statistics"""
    since = datetime.utcnow() - timedelta(hours=hours)
    
    total_alerts = db.query(Alert).filter(Alert.created_at >= since).count()
    resolved_alerts = db.query(Alert).filter(
        Alert.created_at >= since,
        Alert.is_resolved == True
    ).count()
    
    # Count by type
    temp_alerts = db.query(Alert).filter(
        Alert.created_at >= since,
        Alert.alert_type == "temperature"
    ).count()
    
    humidity_alerts = db.query(Alert).filter(
        Alert.created_at >= since,
        Alert.alert_type == "humidity"
    ).count()
    
    aqi_alerts = db.query(Alert).filter(
        Alert.created_at >= since,
        Alert.alert_type == "aqi"
    ).count()
    
    return {
        "total_alerts": total_alerts,
        "resolved_alerts": resolved_alerts,
        "unresolved_alerts": total_alerts - resolved_alerts,
        "by_type": {
            "temperature": temp_alerts,
            "humidity": humidity_alerts,
            "aqi": aqi_alerts
        }
    }