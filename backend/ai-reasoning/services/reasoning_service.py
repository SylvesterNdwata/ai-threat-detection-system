import anthropic
from prompts.alert_explanation import build_alert_explanation_prompt
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def explain_alert(alert: dict) -> str:
    response = client.messages.create(
        model="claude-opus-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": build_alert_explanation_prompt(alert)}],
    )
    
    return next(block.text for block in response.content if block.type == "text")