from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path

# Keep the DB file location stable no matter where the app is started from.
DB_FILE = Path(__file__).resolve().parents[2] / "logs.db"
DATABASE_URL = f"sqlite:///{DB_FILE.as_posix()}"
engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

