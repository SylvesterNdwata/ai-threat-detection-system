from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.logs import router
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to database...")
    from db.database import Base, engine
    Base.metadata.create_all(bind=engine)
    print("Database connected and tables created.")
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

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