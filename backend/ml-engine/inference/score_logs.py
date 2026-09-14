import time
import joblib
import requests
from datetime import datetime, timezone

from utils.feature_function import compute_features

POLL_INTERVAL_SECONDS = 5
LOOKBACK_MINUTES = 20
ALERT_COOLDOWN_MINUTES = 20

def main():
    model = joblib.load("models/isolation_forest.joblib")  # loaded ONCE, not per iteration
    last_alerted_at = {}

    print("ML inference engine started...")
    while True:
        try:
            response = requests.get(
                "http://localhost:8001/logs",
                params={"since_minutes": LOOKBACK_MINUTES},
                timeout=10,
            )
            response.raise_for_status()
            logs = response.json()

            features = compute_features(logs)
            if features.empty:
                print("No logs to score.")
            else:
                predictions = model.predict(features)
                flagged_ips = features.index[predictions == -1]

                now = datetime.now(timezone.utc)
                for ip in flagged_ips:
                    last_alert = last_alerted_at.get(ip)
                    if last_alert and (now - last_alert).total_seconds() < ALERT_COOLDOWN_MINUTES * 60:
                        print(f"SUPPRESSED (cooldown): {ip}")
                        continue

                    alert = {
                        "rule_name": "MLAnomalyDetected",
                        "source_ip": ip,
                        "detail": "Flagged as anomalous by Isolation Forest",
                    }
                    post_response = requests.post("http://localhost:8001/alerts", json=alert, timeout=10)
                    post_response.raise_for_status()
                    print(f"ALERT posted for {ip}")
                    last_alerted_at[ip] = now

        except requests.exceptions.RequestException as e:
            print(f"Inference iteration failed: {e}")

        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
