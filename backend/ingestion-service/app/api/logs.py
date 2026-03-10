from schemas.log_schema import Log
from fastapi import APIRouter


router = APIRouter()


@router.post("/logs")
async def create_log(log: Log):
    return {"message": "Log saved successfully", "log": log}
