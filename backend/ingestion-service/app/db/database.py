"""
Database setup for SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Step 1: Create the database engine
# This is the connection to our SQLite database
DATABASE_URL = "sqlite:///./threat_detection.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Step 2: Create a session factory
# Sessions are how we talk to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Step 3: Create the Base class
# All our database models will inherit from this
Base = declarative_base()


# Step 4: Function to get a database session
def get_db():
    """
    This function provides a database session for each request.
    FastAPI will call this automatically when we use Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db  # Give the session to the endpoint
    finally:
        db.close()  # Always close when done
