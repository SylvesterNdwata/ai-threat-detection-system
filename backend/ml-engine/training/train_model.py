import joblib
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from utils.feature_function import compute_features
from training.generate_training_data import generate_training_logs

logs, anomaly_labels = generate_training_logs(num_anomalous_ips=10, num_normal_ips=300)
features = compute_features(logs)

contamination = len([ip for ip, label in anomaly_labels.items() if label != "normal"]) / len(features)

model = IsolationForest(n_estimators=100, contamination=contamination, random_state=42)
model.fit(features)

predictions = model.predict(features)
flagged_ips = set(features.index[predictions == -1])
actual_anomalous_ips = set([ip for ip, label in anomaly_labels.items() if label != "normal"])

print(f"Flagged {len(flagged_ips)} of {len(features)} IPs as anomalous")
print(f"Correctly caught: {len(flagged_ips & actual_anomalous_ips)} / {len(actual_anomalous_ips)} known anomalies")
print(f"False positives: {flagged_ips - actual_anomalous_ips}")
print(f"False negatives (missed): {actual_anomalous_ips - flagged_ips}")

joblib.dump(model, "models/isolation_forest.joblib")