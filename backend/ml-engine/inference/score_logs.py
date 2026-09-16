import time
import joblib
import requests
import os
from datetime import datetime, timezone

from utils.feature_function import compute_features

POLL_INTERVAL_SECONDS = 5
LOOKBACK_MINUTES = 20
ALERT_COOLDOWN_MINUTES = 20
INGESTION_SERVICE_URL = os.environ.get("INGESTION_SERVICE_URL", "http://localhost:8001")

def main():
    iso_model = joblib.load("models/isolation_forest.joblib")
    rf_model = joblib.load("models/random_forest.joblib")
    last_alerted_at = {}

    print("ML inference engine started...")
    while True:
        try:
            response = requests.get(
                f"{INGESTION_SERVICE_URL}/logs",
                params={"since_minutes": LOOKBACK_MINUTES},
                timeout=10,
            )
            response.raise_for_status()
            logs = response.json()

            features = compute_features(logs)
            if features.empty:
                print("No logs to score.")
            else:
                predictions = iso_model.predict(features)
                flagged_ips = features.index[predictions == -1]

                now = datetime.now(timezone.utc)
                for ip in flagged_ips:
                    last_alert = last_alerted_at.get(ip)
                    if last_alert and (now - last_alert).total_seconds() < ALERT_COOLDOWN_MINUTES * 60:
                        print(f"SUPPRESSED (cooldown): {ip}")
                        continue
                    
                    ip_features = features.loc[[ip]]
                    predicted_type = rf_model.predict(ip_features)[0]
                    confidence = rf_model.predict_proba(ip_features)[0].max()
                    
                    if predicted_type == "normal":
                        detail = f"Flagged as anomalous by Isolation Forest (no known attack pattern matched); Random Forest still called it 'normal' at {confidence:.0%} confidence)"
                    else:
                        detail = f"Flagged as anomalous by Isolation Forest; Random Forest suggests '{predicted_type}' ({confidence:.0%} confidence)"

                    alert = {
                        "rule_name": "MLAnomalyDetected",
                        "source_ip": ip,
                        "detail": detail,
                    }
                    post_response = requests.post(f"{INGESTION_SERVICE_URL}/alerts", json=alert, timeout=10)
                    post_response.raise_for_status()
                    print(f"ALERT posted for {ip}")
                    last_alerted_at[ip] = now

        except requests.exceptions.RequestException as e:
            print(f"Inference iteration failed: {e}")

        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
