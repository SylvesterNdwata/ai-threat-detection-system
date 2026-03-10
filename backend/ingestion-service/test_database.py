"""
Test script to create database tables and save a log
"""
from app.db.database import engine, Base, SessionLocal
from app.models.log_model import LogEntry
from datetime import datetime, timezone

print("=" * 60)
print("Testing Database Setup")
print("=" * 60)

# Step 1: Create all tables
print("\n1. Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created! Check for logs.db file in your directory")

# Step 2: Create a test log entry
print("\n2. Creating a test log entry...")
test_log = LogEntry(
    timestamp=datetime.now(timezone.utc),
    source_ip="192.168.1.100",
    user_id="test_user_123",
    endpoint="/api/login",
    status_code=200,
    user_agent="Mozilla/5.0",
    message="Test login successful"
)
print(f"✅ Created LogEntry object: {test_log.source_ip}")

# Step 3: Save to database
print("\n3. Saving to database...")
db = SessionLocal()
try:
    db.add(test_log)
    db.commit()
    db.refresh(test_log)  # Get the ID that was auto-generated
    print(f"✅ Saved! Auto-generated ID: {test_log.id}")
    print(f"   Created at: {test_log.created_at}")
finally:
    db.close()

# Step 4: Query it back
print("\n4. Querying the log back from database...")
db = SessionLocal()
try:
    saved_log = db.query(LogEntry).filter(LogEntry.id == test_log.id).first()
    if saved_log:
        print(f"✅ Found log in database!")
        print(f"   ID: {saved_log.id}")
        print(f"   IP: {saved_log.source_ip}")
        print(f"   Status: {saved_log.status_code}")
        print(f"   Message: {saved_log.message}")
    else:
        print("❌ Log not found!")
finally:
    db.close()

print("\n" + "=" * 60)
print("✅ Database test complete!")
print("=" * 60)