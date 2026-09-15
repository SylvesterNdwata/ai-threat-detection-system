import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from utils.feature_function import compute_features
from training.generate_training_data import generate_training_logs

logs, anomaly_labels = generate_training_logs(num_anomalous_ips=80, num_normal_ips=300)
features = compute_features(logs)
features["label"] = features.index.map(anomaly_labels)

X = features.drop(columns=["label"])
y = features["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)
print(classification_report(y_test, y_pred))

joblib.dump(rf_model, "models/random_forest.joblib")