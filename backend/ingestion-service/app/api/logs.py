from schemas.log_schema import Log
from fastapi import APIRouter, Depends, HTTPException
from db.database import get_db
from sqlalchemy.orm import Session
from models.log_model import LogEntry



router = APIRouter()

@router.post("/logs")
async def create_log(log: Log, db: Session = Depends(get_db)):
    db_entry = LogEntry(
        timestamp=log.timestamp,
        source_ip=log.source_ip,
        user_id=log.user_id,
        endpoint=log.endpoint,
        status_code=log.status_code,
        user_agent=log.user_agent,
        message=log.message
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return {"message": "Log saved successfully", "log": db_entry.id}
    

@router.get("/logs/{log_id}")
async def get_log(log_id: int, db: Session = Depends(get_db)):
    log_entry = db.query(LogEntry).filter(LogEntry.id == log_id).first()
    if not log_entry:
        raise HTTPException(status_code=404, detail="Log entry not found")
    return {
        "id": log_entry.id,
        "timestamp": log_entry.timestamp,
        "source_ip": log_entry.source_ip,
        "user_id": log_entry.user_id,
        "endpoint": log_entry.endpoint,
        "status_code": log_entry.status_code,
        "user_agent": log_entry.user_agent,
        "message": log_entry.message
    }

@router.get("/logs")
async def list_logs(db: Session = Depends(get_db)):
    log_entries = db.query(LogEntry).all()
    
    return [
        {
            "id": log_entry.id,
            "timestamp": log_entry.timestamp,
            "source_ip": log_entry.source_ip,
            "user_id": log_entry.user_id,
            "endpoint": log_entry.endpoint,
            "status_code": log_entry.status_code,
            "user_agent": log_entry.user_agent,
            "message": log_entry.message
        }
        for log_entry in log_entries
    ]