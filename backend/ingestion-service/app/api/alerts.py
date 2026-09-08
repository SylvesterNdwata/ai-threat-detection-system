from datetime import timezone

from fastapi import APIRouter, Depends
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
            "detected_at": a.detected_at.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
        }
        for a in alert_entries
    ]