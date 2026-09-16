from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path

# Keep the DB file location stable no matter where the app is started from.
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
try:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
except TypeError:
    DATA_DIR.mkdir(parents=True)
DB_FILE = DATA_DIR / "logs.db"
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

