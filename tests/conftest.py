import os
from collections.abc import Generator
from unittest.mock import Mock

os.environ["DATABASE_URL"] = "sqlite:////tmp/oficina_test.db"
os.environ["JWT_SECRET"] = "test-secret"

import pytest
from fastapi.testclient import TestClient

from app.infrastructure.database import Base, engine
from app.main import app
from tests.factories import client_payload, part_payload, service_payload, vehicle_payload


@pytest.fixture(autouse=True)
def clean_db() -> Generator[None, None, None]:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def token(client: TestClient) -> str:
    response = client.post(
        "/api/v1/auth/token",
        json={"email": "admin@oficina.example.com", "password": "Admin123!"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def notification_mock(monkeypatch: pytest.MonkeyPatch) -> Mock:
    mock = Mock()
    monkeypatch.setattr("app.application.order_service.notify_status", mock)
    return mock


@pytest.fixture
def catalog(client: TestClient, auth: dict[str, str]) -> dict[str, dict]:
    created_client = client.post("/api/v1/clients", headers=auth, json=client_payload()).json()
    vehicle = client.post(
        "/api/v1/vehicles",
        headers=auth,
        json=vehicle_payload(created_client["id"]),
    ).json()
    service = client.post("/api/v1/services", headers=auth, json=service_payload()).json()
    part = client.post("/api/v1/parts", headers=auth, json=part_payload()).json()
    return {"client": created_client, "vehicle": vehicle, "service": service, "part": part}
