from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, CustomAlert, UserCity

router = APIRouter()

class CustomAlertCreate(BaseModel):
    city: str
    alert_type: str
    threshold_value: float
    email_enabled: bool = True
    sms_enabled: bool = False

class CustomAlertResponse(BaseModel):
    id: int
    city: str
    alert_type: str
    threshold_value: float
    is_active: bool
    email_enabled: bool
    sms_enabled: bool
    
    class Config:
        from_attributes = True

class UserCityCreate(BaseModel):
    city: str
    latitude: float
    longitude: float
    is_favorite: bool = False

class UserCityResponse(BaseModel):
    id: int
    city: str
    latitude: float
    longitude: float
    is_favorite: bool
    
    class Config:
        from_attributes = True

@router.post("/alerts", response_model=CustomAlertResponse)
async def create_custom_alert(
    alert: CustomAlertCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_alert = CustomAlert(
        user_id=current_user.id,
        **alert.dict()
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.get("/alerts", response_model=List[CustomAlertResponse])
async def get_user_alerts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    alerts = db.query(CustomAlert).filter(
        CustomAlert.user_id == current_user.id
    ).all()
    return alerts

@router.put("/alerts/{alert_id}")
async def update_custom_alert(
    alert_id: int,
    alert_update: CustomAlertCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    alert = db.query(CustomAlert).filter(
        CustomAlert.id == alert_id,
        CustomAlert.user_id == current_user.id
    ).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    for key, value in alert_update.dict().items():
        setattr(alert, key, value)
    
    db.commit()
    return {"message": "Alert updated successfully"}

@router.delete("/alerts/{alert_id}")
async def delete_custom_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    alert = db.query(CustomAlert).filter(
        CustomAlert.id == alert_id,
        CustomAlert.user_id == current_user.id
    ).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    db.delete(alert)
    db.commit()
    return {"message": "Alert deleted successfully"}

@router.post("/cities", response_model=UserCityResponse)
async def add_user_city(
    city: UserCityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_city = UserCity(
        user_id=current_user.id,
        **city.dict()
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

@router.get("/cities", response_model=List[UserCityResponse])
async def get_user_cities(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cities = db.query(UserCity).filter(
        UserCity.user_id == current_user.id
    ).all()
    return cities

@router.delete("/cities/{city_id}")
async def delete_user_city(
    city_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    city = db.query(UserCity).filter(
        UserCity.id == city_id,
        UserCity.user_id == current_user.id
    ).first()
    
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    
    db.delete(city)
    db.commit()
    return {"message": "City removed successfully"}