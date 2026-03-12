from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone


class Log(BaseModel):
    timestamp: datetime
    source_ip: str = Field(..., max_length = 45, description = "Source IP address (IPv4 or IPv6)")
    user_id: str | None = Field(None, max_length=50, description="User ID")
    endpoint: str = Field(..., max_length=255, description="API endpoint")
    status_code: int = Field(..., ge=100, le=599, description="HTTP status code")
    user_agent: str | None = Field(None, max_length=255, description="User agent string")
    message: str = Field(..., max_length=1000, description="Log message content")
    
    @field_validator("timestamp")
    @classmethod
    def normalize_timestamp(cls, value):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        else:
            value = value.astimezone(timezone.utc)
        return value