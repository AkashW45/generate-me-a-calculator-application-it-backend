import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestHealth:
    def test_health_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

class TestAdd:
    def test_add_positive(self):
        response = client.get("/add?a=10&b=20")
        assert response.status_code == 200
        assert response.json() == {"result": 30.0}

    def test_add_negative(self):
        response = client.get("/add?a=-5.5&b=-2.5")
        assert response.status_code == 200
        assert response.json() == {"result": -8.0}

    def test_add_mixed_signs(self):
        response = client.get("/add?a=-10&b=5")
        assert response.status_code == 200
        assert response.json() == {"result": -5.0}

class TestSubtract:
    def test_subtract_positive(self):
        response = client.get("/subtract?a=50&b=20")
        assert response.status_code == 200
        assert response.json() == {"result": 30.0}

class TestMultiply:
    def test_multiply_basic(self):
        response = client.get("/multiply?a=3&b=4")
        assert response.status_code == 200
        assert response.json() == {"result": 12.0}

    def test_multiply_by_zero(self):
        response = client.get("/multiply?a=10&b=0")
        assert response.status_code == 200
        assert response.json() == {"result": 0.0}

class TestDivide:
    def test_divide_basic(self):
        response = client.get("/divide?a=100&b=4")
        assert response.status_code == 200
        assert response.json() == {"result": 25.0}

    def test_divide_by_zero(self):
        response = client.get("/divide?a=10&b=0")
        assert response.status_code == 400
        assert response.json() == {"detail": "Division by zero is not allowed"}

    def test_divide_negative(self):
        response = client.get("/divide?a=-20&b=5")
        assert response.status_code == 200
        assert response.json() == {"result": -4.0}

class TestPower:
    def test_power_positive_integers(self):
        response = client.get("/power?a=2&b=3")
        assert response.status_code == 200
        assert response.json() == {"result": 8.0}

    def test_power_zero_exponent(self):
        response = client.get("/power?a=5&b=0")
        assert response.status_code == 200
        assert response.json() == {"result": 1.0}

    def test_power_negative_exponent(self):
        response = client.get("/power?a=2&b=-2")
        assert response.status_code == 200
        assert response.json() == {"result": 0.25}

    def test_power_fractional_exponent(self):
        response = client.get("/power?a=9&b=0.5")
        assert response.status_code == 200
        assert response.json() == {"result": 3.0}

    def test_power_large_numbers(self):
        response = client.get("/power?a=2&b=30")
        assert response.status_code == 200
        data = response.json()
        assert data["result"] == pytest.approx(1073741824.0)

# Edge cases for parameter types
class TestInvalidParameters:
    def test_add_missing_parameters(self):
        response = client.get("/add?a=5")
        assert response.status_code == 422  # FastAPI validation error

    def test_add_non_numeric(self):
        response = client.get("/add?a=abc&b=def")
        assert response.status_code == 422

    def test_divide_invalid_input(self):
        response = client.get("/divide?a=hello&b=world")
        assert response.status_code == 422