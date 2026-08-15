from typing import Any

from fastapi.testclient import TestClient

from app.main import app


client: Any = TestClient(app)


def test_chat():
    response = client.post(
        "/chat",
        json={
            "message": "What is Python?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert isinstance(data["answer"], str)


def test_chat_validation():
    response = client.post(
        "/chat",
        json={
            "message": ""
        }
    )

    assert response.status_code == 422