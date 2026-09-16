import anthropic
import requests
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.reasoning_service import explain_alert

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

INGESTION_SERVICE_URL = os.environ.get("INGESTION_SERVICE_URL", "http://localhost:8001")

@app.get("/explain/{alert_id}")
async def explain(alert_id: int):
    try:
        response = requests.get(f"{INGESTION_SERVICE_URL}/alerts/{alert_id}", timeout=10)
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=502, detail="Could not reach ingestion service")

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Alert not found")
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise HTTPException(status_code=502, detail="Ingestion service returned an error")

    alert = response.json()

    try:
        explanation = explain_alert(alert)
    except anthropic.RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limited by Claude API, try again shortly")
    except anthropic.AuthenticationError:
        raise HTTPException(status_code=500, detail="Claude API authentication failed, check ANTHROPIC_API_KEY")
    except anthropic.APIStatusError as e:
        raise HTTPException(status_code=502, detail=f"Claude API error: {e.message}")
    except anthropic.APIConnectionError:
        raise HTTPException(status_code=502, detail="Could not reach Claude API")

    return {"alert_id": alert_id, "explanation": explanation}
