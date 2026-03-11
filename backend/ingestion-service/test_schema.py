"""
Quick test script to learn Pydantic validation
"""
from app.schemas.log_schema import Log
from datetime import datetime

print("=" * 60)
print("Testing Pydantic Log Schema")
print("=" * 60)

# Test 1: Valid log
print("\n✅ Test 1: Creating a VALID log...")
try:
    valid_log = Log(
        timestamp=datetime.now(),
        source_ip="192.168.1.100",
        endpoint="/api/login",
        status_code=200,  # Valid HTTP code
        message="Login successful",
        user_id="user123",
        user_agent="Mozilla/5.0"
    )
    print(f"Success! Created log with status {valid_log.status_code}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Invalid status code (too high)
print("\n❌ Test 2: Creating log with INVALID status code (999)...")
try:
    invalid_log = Log(
        timestamp=datetime.now(),
        source_ip="192.168.1.100",
        endpoint="/api/test",
        status_code=999,  # Invalid - too high!
        message="Test",
        user_id="user123",
        user_agent="Mozilla/5.0"
    )
    print("Success!")
except Exception as e:
    print(f"Validation Error (as expected): {e}")

# Test 3: Invalid status code (too low)
print("\n❌ Test 3: Creating log with INVALID status code (50)...")
try:
    invalid_log2 = Log(
        timestamp=datetime.now(),
        source_ip="192.168.1.100",
        endpoint="/api/test",
        status_code=50,  # Invalid - too low!
        message="Test",
        user_id="user123",
        user_agent="Mozilla/5.0"
    )
    print("Success!")
except Exception as e:
    print(f"Validation Error (as expected): {e}")

print("\n" + "=" * 60)
print("Testing complete! Notice how Pydantic automatically validates.")
print("=" * 60)
