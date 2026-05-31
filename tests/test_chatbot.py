from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_chatbot_returns_available_activities():
    response = client.post("/chatbot", json={"message": "What activities are available?"})

    assert response.status_code == 200
    assert "Available activities:" in response.json()["response"]


def test_chatbot_rejects_blank_message():
    response = client.post("/chatbot", json={"message": "   "})

    assert response.status_code == 400
    assert response.json()["detail"] == "Message cannot be empty"


def test_chatbot_returns_greeting_message():
    response = client.post("/chatbot", json={"message": "Hello there"})

    assert response.status_code == 200
    assert "I can help with school activities" in response.json()["response"]
