from utils.feature_function import compute_features
from training.generate_training_data import generate_training_logs

import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

logs, anomaly_labels = generate_training_logs(num_normal_ips=300, num_anomalous_ips=10)
anomalous_ips = [ip for ip, label in anomaly_labels.items() if label != "normal"]
print(f"Total log entries: {len(logs)}")
print(f"Total distinct IPs generated: {len(set(l['source_ip'] for l in logs))}")
print(f"Anomalous IPs injected: {anomalous_ips}")
print()

features = compute_features(logs)
print(f"Feature table shape: {features.shape}")
print()

print("=== Anomalous IP rows ===")
print(features.loc[features.index.isin(anomalous_ips)])
print()

print("=== Normal traffic summary (mean/std) ===")
normal_features = features.loc[~features.index.isin(anomalous_ips)]
print(normal_features.describe())
