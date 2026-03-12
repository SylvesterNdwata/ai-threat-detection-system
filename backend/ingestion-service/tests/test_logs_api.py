from datetime import datetime, timezone

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.logs import router
from db.database import Base, get_db
from models.log_model import LogEntry


@pytest.fixture()
def client(tmp_path):
    db_file = tmp_path / "api_test.db"
    engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    Base.metadata.create_all(bind=engine, tables=[LogEntry.__table__])

    app = FastAPI()
    app.include_router(router)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine, tables=[LogEntry.__table__])
    engine.dispose()


def make_payload(**overrides):
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_ip": "192.168.1.10",
        "user_id": "user123",
        "endpoint": "/api/login",
        "status_code": 401,
        "user_agent": "Mozilla/5.0",
        "message": "Login failed",
    }
    payload.update(overrides)
    return payload


def test_post_logs_returns_200_and_created_id(client):
    response = client.post("/logs", json=make_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Log saved successfully"
    assert isinstance(body["log"], int)


def test_post_logs_returns_422_for_invalid_payload(client):
    response = client.post("/logs", json=make_payload(status_code=999))

    assert response.status_code == 422


def test_post_logs_returns_422_for_source_ip_too_long(client):
    response = client.post("/logs", json=make_payload(source_ip="x" * 46))

    assert response.status_code == 422


def test_get_log_by_id_returns_200_for_existing_log(client):
    create_response = client.post("/logs", json=make_payload(source_ip="10.0.0.5"))
    log_id = create_response.json()["log"]

    response = client.get(f"/logs/{log_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == log_id
    assert body["source_ip"] == "10.0.0.5"


def test_get_log_by_id_returns_404_for_missing_log(client):
    response = client.get("/logs/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Log entry not found"


def test_get_logs_returns_list(client):
    client.post("/logs", json=make_payload(source_ip="10.0.0.1", message="first"))
    client.post("/logs", json=make_payload(source_ip="10.0.0.2", message="second"))

    response = client.get("/logs")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 2
    assert {item["source_ip"] for item in body} == {"10.0.0.1", "10.0.0.2"}
