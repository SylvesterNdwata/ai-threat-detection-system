from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from db.database import Base

class AlertEntry(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_name = Column(String(255), nullable=False, index=True)
    source_ip = Column(String(45), nullable=True)
    detail = Column(String(1024), nullable=False)
    detected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)