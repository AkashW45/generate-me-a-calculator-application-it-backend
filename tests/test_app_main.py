import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_arithmetic_operations(client):
    # Test addition
    resp = client.get("/add", params={"a": 3, "b": 4})
    assert resp.status_code == 200
    assert resp.json()["result"] == 7.0

    # Test subtraction
    resp = client.get("/subtract", params={"a": 10, "b": 3})
    assert resp.status_code == 200
    assert resp.json()["result"] == 7.0

    # Test multiplication
    resp = client.get("/multiply", params={"a": 3, "b": 5})
    assert resp.status_code == 200
    assert resp.json()["result"] == 15.0

    # Test power
    resp = client.get("/power", params={"a": 2, "b": 3})
    assert resp.status_code == 200
    assert resp.json()["result"] == 8.0

def test_divide_success(client):
    resp = client.get("/divide", params={"a": 10, "b": 2})
    assert resp.status_code == 200
    assert resp.json()["result"] == 5.0

def test_divide_by_zero(client):
    resp = client.get("/divide", params={"a": 10, "b": 0})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Division by zero is not allowed"

def test_missing_query_param(client):
    resp = client.get("/add", params={"a": 10})
    assert resp.status_code == 422