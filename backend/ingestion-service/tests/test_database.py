from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database import Base
from models.log_model import LogEntry


def test_can_save_and_read_a_log_entry(tmp_path):
    db_file = tmp_path / "test_logs.db"
    engine = create_engine(f"sqlite:///{db_file}")
    SessionLocal = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine, tables=[LogEntry.__table__])

    session = SessionLocal()
    try:
        entry = LogEntry(
            timestamp=datetime.now(timezone.utc),
            source_ip="192.168.1.100",
            user_id="test_user_123",
            endpoint="/api/login",
            status_code=200,
            user_agent="Mozilla/5.0",
            message="Test login successful",
        )

        session.add(entry)
        session.commit()
        session.refresh(entry)

        saved_entry = session.query(LogEntry).filter(LogEntry.id == entry.id).first()
        
        assert saved_entry is not None
        assert saved_entry.id == entry.id
        assert saved_entry.source_ip == "192.168.1.100"
        assert saved_entry.status_code == 200
        assert saved_entry.message == "Test login successful"
        assert saved_entry.created_at is not None
    finally:
        session.close()
        engine.dispose()
