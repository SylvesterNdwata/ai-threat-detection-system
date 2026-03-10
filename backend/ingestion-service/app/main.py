from fastapi import FastAPI
from api.logs import router
import uvicorn

app = FastAPI()

app.include_router(router)

@app.get("/")
async def root():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=8001
    )