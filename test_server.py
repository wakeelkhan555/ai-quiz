import server
from fastapi.testclient import TestClient

client = TestClient(server.app)


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200


def test_get_questions():
    response = client.get("/questions")
    assert response.status_code == 200
    assert len(response.json()) == 20


def test_check_correct_answer(monkeypatch):
    monkeypatch.setattr(
        server,
        "generate_fun_fact",
        lambda question: "This is a test fun fact."
    )

    response = client.post(
        "/check-answer",
        json={
            "question": "What is the capital of France?",
            "user_answer": "Paris"
        }
    )

    assert response.status_code == 200
    assert response.json()["correct"] is True
    assert response.json()["score"] == 1


def test_check_wrong_answer(monkeypatch):
    monkeypatch.setattr(
        server,
        "generate_fun_fact",
        lambda question: "This is a test fun fact."
    )

    response = client.post(
        "/check-answer",
        json={
            "question": "What is the capital of France?",
            "user_answer": "London"
        }
    )

    assert response.status_code == 200
    assert response.json()["correct"] is False
    assert response.json()["score"] == 0
