from datetime import timezone

from fastapi import APIRouter, Depends, HTTPException
from api.logs import normalize_timestamp
from db.database import get_db
from models.alert_model import AlertEntry
from schemas.alert_schema import Alert
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/alerts")
async def create_alert(alert: Alert, db: Session = Depends(get_db)):
    db_entry = AlertEntry(
        rule_name=alert.rule_name,
        source_ip=alert.source_ip,
        detail=alert.detail
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    
    return {"message": "Alert saved successfully", "alert": db_entry.id}

@router.get("/alerts")
async def list_alerts(db: Session = Depends(get_db)):
    alert_entries = db.query(AlertEntry).all()
    return [
        {
            "id": a.id,
            "rule_name": a.rule_name,
            "source_ip": a.source_ip,
            "detail": a.detail,
            "detected_at": normalize_timestamp(a.detected_at)
        }
        for a in alert_entries
    ]
    
@router.get("/alerts/{alert_id}")
async def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert_entry = db.query(AlertEntry).filter(AlertEntry.id == alert_id).first()
    if not alert_entry:
        raise HTTPException(status_code=404, detail="Alert entry not found")
    return {
        "id": alert_entry.id,
        "rule_name": alert_entry.rule_name,
        "source_ip": alert_entry.source_ip,
        "detail": alert_entry.detail,
        "detected_at": normalize_timestamp(alert_entry.detected_at),
    }