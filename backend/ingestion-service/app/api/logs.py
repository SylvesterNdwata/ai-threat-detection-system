from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class Log(BaseModel):
    timestamp: datetime
    source_ip: str
    user_id: str | None = None
    endpoint: str
    status_code: int
    user_agent: str | None = None
    message: str
    

@app.post("/logs/")
async def create_log(log: Log):
    # Save the log to a database or perform any necessary processing
    print(log)
    return {"message": "Log saved successfully"}

@app.put("logs/{log_id}")
async def update_log(log_id: int, log: Log):
    return {"log_id": log_id, **log.model_dump()}