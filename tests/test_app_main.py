from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_add():
    response = client.get("/add?a=2&b=3")
    assert response.status_code == 200
    assert response.json() == {"result": 5.0}


def test_divide_happy():
    response = client.get("/divide?a=10&b=2")
    assert response.status_code == 200
    assert response.json() == {"result": 5.0}


def test_divide_by_zero():
    response = client.get("/divide?a=10&b=0")
    assert response.status_code == 400
    assert response.json() == {"detail": "Division by zero is not allowed"}


def test_calculator_ui():
    response = client.get("/calculator")
    assert response.status_code == 200
    assert "Modern Calculator" in response.text
    assert "Bootstrap" in response.text
    assert "calculate()" in response.text


def test_add_missing_param():
    response = client.get("/add?a=1")
    assert response.status_code == 422