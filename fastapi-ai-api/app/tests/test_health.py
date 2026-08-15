from typing import Any

from fastapi.testclient import TestClient

from app.main import app


client: Any = TestClient(app)


def test_health():
    response: Any = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"
    assert "timestamp" in data