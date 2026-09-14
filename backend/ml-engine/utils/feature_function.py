import pandas as pd

def compute_features(logs: list[dict]) -> pd.DataFrame:
    """
    Compute features from a list of log entries.
    
    Args:
        logs (list[dict]): List of log entries, each represented as a dictionary.
        
    Returns:
        pd.DataFrame: DataFrame containing computed features for each log entry. 
    """
    df = pd.DataFrame(logs)
    
    if df.empty:
        return pd.DataFrame()
    
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["is_error"] = df["status_code"] >= 400
    
    grouped = df.groupby("source_ip")
    features = grouped.agg(
        request_count=("id", "count"),
        distinct_endpoints=("endpoint", "nunique"),
        error_ratio=("is_error", "mean"),
        distinct_user_ids=("user_id", "nunique"),
        distinct_user_agents=("user_agent", "nunique"),
        first_seen=("timestamp", "min"),
        last_seen=("timestamp", "max")
    )
    
    span_minutes = (features["last_seen"] - features["first_seen"]).dt.total_seconds() / 60
    features["requests_per_minute"] = features["request_count"] / span_minutes.replace(0, 1)
    
    return features.drop(columns=["first_seen", "last_seen"])