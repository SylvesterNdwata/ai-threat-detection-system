from datetime import datetime

import pytest
from pydantic import ValidationError

from schemas.log_schema import Log


def make_log(**overrides):
    payload = {
        "timestamp": datetime(2026, 3, 12, 10, 0, 0),
        "source_ip": "192.168.1.100",
        "user_id": "user123",
        "endpoint": "/api/login",
        "status_code": 401,
        "user_agent": "Mozilla/5.0",
        "message": "Login failed",
    }
    payload.update(overrides)
    return Log(**payload)


def test_accepts_a_valid_log():
    log = make_log()

    assert log.source_ip == "192.168.1.100"
    assert log.status_code == 401
    assert log.message == "Login failed"


@pytest.mark.parametrize("status_code", [50, 999])
def test_rejects_status_codes_outside_http_range(status_code):
    with pytest.raises(ValidationError):
        make_log(status_code=status_code)


def test_rejects_source_ip_longer_than_45_characters():
    with pytest.raises(ValidationError):
        make_log(source_ip="x" * 46)


def test_rejects_endpoint_longer_than_255_characters():
    with pytest.raises(ValidationError):
        make_log(endpoint="/api/" + ("x" * 300))


def test_rejects_message_longer_than_1000_characters():
    with pytest.raises(ValidationError):
        make_log(message="x" * 1001)


def test_allows_optional_fields_to_be_missing():
    log = make_log(user_id=None, user_agent=None)

    assert log.user_id is None
    assert log.user_agent is None


def test_can_be_serialized_to_json():
    log = make_log(status_code=403, message="Access denied")
    json_output = log.model_dump_json()

    assert '"status_code":403' in json_output
    assert '"message":"Access denied"' in json_output
