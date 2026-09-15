import random
from datetime import datetime, timedelta, timezone

NORMAL_ENDPOINTS = ["/api/data", "/api/logout", "/health", "/metrics", "/api/profile"]
USER_AGENTS = ["Mozilla/5.0", "PostmanRuntime/7.28.4"]
USERNAMES = ["silver", "admin", "guest", "alice", "bob"]

def generate_normal_ip_logs(ip, next_id, base_time):
    logs = []
    request_count = random.randint(1, 15)
    user_id = random.choice(USERNAMES + [None])
    user_agent = random.choice(USER_AGENTS)
    for _ in range(request_count):
        timestamp = base_time + timedelta(seconds=random.uniform(0, 900))
        logs.append({
            "id": next_id,
            "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
            "source_ip": ip,
            "user_id": user_id,
            "endpoint": random.choice(NORMAL_ENDPOINTS),
            "status_code": random.choices([200, 201, 404], weights=[85, 10, 5])[0],
            "user_agent": user_agent,
            "message": "OK",
        })
        next_id += 1
    return logs, next_id

def generate_anomalous_ip_logs(ip, next_id, base_time, kind):
    logs = []
    if kind == "credential_stuffing":
        for i in range(8):
            timestamp = base_time + timedelta(seconds=i * 5)
            logs.append({
                "id": next_id, "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
                "source_ip": ip, "user_id": f"user{i}", "endpoint": "/api/login",
                "status_code": 401, "user_agent": "python-requests/2.28", "message": "Failed login",
            })
            next_id += 1
    elif kind == "port_scan":
        endpoints = ["/api/data", "/api/admin", "/api/internal", "/health", "/metrics", "/config", "/backup"]
        for i, ep in enumerate(endpoints):
            timestamp = base_time + timedelta(seconds=i * 3)
            logs.append({
                "id": next_id, "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
                "source_ip": ip, "user_id": None, "endpoint": ep,
                "status_code": 200, "user_agent": "curl/7.68.0", "message": "OK",
            })
            next_id += 1
    elif kind == "high_rate":
        for i in range(50):
            timestamp = base_time + timedelta(seconds=i * 0.5)
            logs.append({
                "id": next_id, "timestamp": timestamp.isoformat().replace("+00:00", "Z"),
                "source_ip": ip, "user_id": "bot", "endpoint": "/api/data",
                "status_code": 200, "user_agent": "python-requests/2.28", "message": "OK",
            })
            next_id += 1
    return logs, next_id

def generate_training_logs(num_normal_ips=300, num_anomalous_ips=10):
    logs = []
    anomaly_labels = {}
    next_id = 1
    base_time = datetime.now(timezone.utc)

    for _ in range(num_normal_ips):
        ip = f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        ip_logs, next_id = generate_normal_ip_logs(ip, next_id, base_time)
        logs.extend(ip_logs)
        anomaly_labels[ip] = "normal"

    kinds = ["credential_stuffing", "port_scan", "high_rate"]
    for i in range(num_anomalous_ips):
        ip = f"203.0.113.{i+1}"
        kind = random.choice(kinds)
        ip_logs, next_id = generate_anomalous_ip_logs(ip, next_id, base_time, kind)
        logs.extend(ip_logs)
        anomaly_labels[ip] = kind

    return logs, anomaly_labels
