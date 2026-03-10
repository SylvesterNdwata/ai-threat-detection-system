from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from db.database import Base


class LogEntry(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    source_ip = Column(String(45), nullable=False)
    user_id = Column(String(50), nullable=True)
    endpoint = Column(String(255), nullable=False)
    status_code = Column(Integer, nullable=False)
    user_agent = Column(String(255), nullable=True)
    message = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))