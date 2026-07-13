import os

os.environ["DATABASE_URL"] = "sqlite:////tmp/oficina_test.db"
os.environ["JWT_SECRET"] = "test-secret"
import pytest
from fastapi.testclient import TestClient

from app.infrastructure.database import Base, engine
from app.main import app


@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def token(client):
    r = client.post(
        "/api/v1/auth/token", json={"email": "admin@oficina.example.com", "password": "Admin123!"}
    )
    return r.json()["access_token"]


@pytest.fixture
def auth(token):
    return {"Authorization": f"Bearer {token}"}
