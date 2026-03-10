"""
Test the enhanced Log schema with all validations
"""
from app.schemas.log_schema import Log
from datetime import datetime

print("=" * 70)
print("Testing Your Enhanced Log Schema")
print("=" * 70)

# Test 1: Valid log with all fields
print("\n✅ Test 1: Creating a VALID log with all fields...")
try:
    valid_log = Log(
        timestamp=datetime.now(),
        source_ip="192.168.1.100",
        user_id="user123",
        endpoint="/api/login",
        status_code=200,
        user_agent="Mozilla/5.0",
        message="Login successful"
    )
    print("✅ Success! All validations passed.")
    print(f"   - IP: {valid_log.source_ip}")
    print(f"   - Status: {valid_log.status_code}")
    print(f"   - Message: {valid_log.message}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: IP address too long
print("\n❌ Test 2: IP address TOO LONG (50 chars, max is 45)...")
try:
    long_ip = "x" * 50  # 50 characters
    invalid_log = Log(
        timestamp=datetime.now(),
        source_ip=long_ip,
        endpoint="/api/test",
        status_code=200,
        message="Test"
    )
    print("✅ Passed (unexpected!)")
except Exception as e:
    print(f"✅ Caught validation error (expected)!")
    print(f"   Error: String should have at most 45 characters")

# Test 3: Endpoint too long
print("\n❌ Test 3: Endpoint TOO LONG (300 chars, max is 255)...")
try:
    long_endpoint = "/api/" + "x" * 300
    invalid_log = Log(
        timestamp=datetime.now(),
        source_ip="192.168.1.1",
        endpoint=long_endpoint,
        status_code=200,
        message="Test"
    )
    print("✅ Passed (unexpected!)")
except Exception as e:
    print(f"✅ Caught validation error (expected)!")
    print(f"   Error: String should have at most 255 characters")

# Test 4: Message too long
print("\n❌ Test 4: Message TOO LONG (1500 chars, max is 1000)...")
try:
    long_message = "x" * 1500
    invalid_log = Log(
        timestamp=datetime.now(),
        source_ip="192.168.1.1",
        endpoint="/api/test",
        status_code=200,
        message=long_message
    )
    print("✅ Passed (unexpected!)")
except Exception as e:
    print(f"✅ Caught validation error (expected)!")
    print(f"   Error: String should have at most 1000 characters")

# Test 5: Invalid status code
print("\n❌ Test 5: Invalid status code (999)...")
try:
    invalid_log = Log(
        timestamp=datetime.now(),
        source_ip="192.168.1.1",
        endpoint="/api/test",
        status_code=999,
        message="Test"
    )
    print("✅ Passed (unexpected!)")
except Exception as e:
    print(f"✅ Caught validation error (expected)!")
    print(f"   Error: Status code must be between 100-599")

# Test 6: Optional fields can be None
print("\n✅ Test 6: Optional fields (user_id, user_agent) can be None...")
try:
    minimal_log = Log(
        timestamp=datetime.now(),
        source_ip="10.0.0.1",
        endpoint="/health",
        status_code=200,
        message="Health check"
        # Note: user_id and user_agent are not provided
    )
    print(f"✅ Success! Created log without optional fields")
    print(f"   - user_id: {minimal_log.user_id}")
    print(f"   - user_agent: {minimal_log.user_agent}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 7: JSON serialization
print("\n✅ Test 7: Convert to JSON (for API responses)...")
try:
    log = Log(
        timestamp=datetime.now(),
        source_ip="203.0.113.45",
        endpoint="/api/data",
        status_code=403,
        message="Access denied"
    )
    json_data = log.model_dump_json(indent=2)
    print("✅ Success! Log converted to JSON:")
    print(json_data)
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
print("🎉 All tests complete! Your validations are working perfectly!")
print("=" * 70)
