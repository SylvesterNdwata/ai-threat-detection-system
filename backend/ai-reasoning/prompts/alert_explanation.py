def build_alert_explanation_prompt(alert: dict) -> str:
    return f"""You are a security analyst assistant. Explain the following alert in plain
language for someone who may not be a security expert, and suggest what they should check
or do next.

Rule triggered: {alert['rule_name']}
Source IP: {alert['source_ip'] or 'N/A (not IP-specific)'}
Detail: {alert['detail']}
Detected at: {alert['detected_at']}

Keep your explanation concise and actionable."""