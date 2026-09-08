from pydantic import BaseModel, Field

class Alert(BaseModel):
    rule_name: str = Field(..., max_length=100)
    source_ip: str | None = Field(None, max_length=45)
    detail: str = Field(..., max_length=1024)