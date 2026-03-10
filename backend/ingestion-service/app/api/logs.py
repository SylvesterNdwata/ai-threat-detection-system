from schemas.log_schema import Log
from fastapi import APIRouter, Depends
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
async def get_log(log_id):
    return {"log_id": log_id}