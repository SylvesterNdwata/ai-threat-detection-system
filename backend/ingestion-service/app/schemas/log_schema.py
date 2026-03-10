from pydantic import BaseModel, Field
from datetime import datetime


class Log(BaseModel):
    timestamp: datetime
    source_ip: str = Field(..., max_length = 45, description = "Source IP address (IPv4 or IPv6)")
    user_id: str | None = Field(None, max_length=50, description="User ID")
    endpoint: str = Field(..., max_length=255, description="API endpoint")
    status_code: int = Field(..., ge=100, le=599, description="HTTP status code")
    user_agent: str | None = Field(None, max_length=255, description="User agent string")
    message: str = Field(..., max_length=1000, description="Log message content")