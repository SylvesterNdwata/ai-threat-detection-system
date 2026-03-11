import requests
import random
from datetime import datetime, timezone
import time

ENDPOINT = "http://localhost:8001/logs"

def send_log():
    log = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_ip": f"192.168.1.{random.randint(1, 255)}",
        "user_id": random.choice(["silver", "admin", "guest", None]),
        "endpoint": random.choice(["/api/login", "/api/data", "/api/logout", "/admin", "/login"]),
        "status_code": random.choice([200, 201, 400, 401, 403, 404, 500]),
        "user_agent": random.choice(["Mozilla/5.0", "curl/7.68.0", "PostmanRuntime/7.28.4", None]),
        "message": random.choice(["OK", "Login successful", "Data retrieved", "Unauthorized access", "Failed login", "Access denied"])
    }
    try:
        response = requests.post(ENDPOINT, json=log, timeout=5)
        if response.status_code == 200:
            print(f"Log sent successfully: {log}")
        else:
            print(f"Failed to send log: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending log: {e}")

def get_delay_and_burst_state(burst_remaining: int) -> tuple[float, int]:
    if burst_remaining > 0:
        return random.uniform(0.02, 0.15), burst_remaining - 1  # Fast burst
    
    roll = random.random()
    
    if roll < 0.12:
        burst_len = random.randint(10, 30)
        return random.uniform(0.02, 0.15), burst_len -1
    
    if roll < 0.15:
        return random.uniform(2.0, 5.0), 0  

    return random.uniform(0.4, 1.2), 0

if __name__ == "__main__":
    burst_remaining = 0
    for _ in range(30):
        send_log()
        delay, burst_remaining = get_delay_and_burst_state(burst_remaining)
        time.sleep(delay)
        
        
