from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_add():
    response = client.get("/add?a=3&b=4")
    assert response.status_code == 200
    assert response.json() == {"result": 7.0}


def test_subtract():
    response = client.get("/subtract?a=10&b=3")
    assert response.status_code == 200
    assert response.json() == {"result": 7.0}


def test_multiply():
    response = client.get("/multiply?a=2&b=5")
    assert response.status_code == 200
    assert response.json() == {"result": 10.0}


def test_divide():
    response = client.get("/divide?a=10&b=2")
    assert response.status_code == 200
    assert response.json() == {"result": 5.0}


def test_divide_by_zero():
    response = client.get("/divide?a=10&b=0")
    assert response.status_code == 400
    assert response.json()["detail"] == "Division by zero is not allowed"


def test_power():
    response = client.get("/power?a=2&b=3")
    assert response.status_code == 200
    assert response.json() == {"result": 8.0}


def test_missing_params():
    response = client.get("/add")
    assert response.status_code == 422  # validation error


def test_index_page():
    """Test that the main page loads the keypad UI with digit/operator buttons and input/output displays."""
    response = client.get("/")
    assert response.status_code == 200
    # Check that Bootstrap is still present (UI upgrade)
    assert "bootstrap" in response.text.lower()
    # Check for two display areas (input expression and output result)
    assert "input-expression" in response.text.lower() or "input expression" in response.text.lower()
    assert "output-result" in response.text.lower() or "output result" in response.text.lower()
    # Check for digit buttons 0-9
    for digit in "0123456789":
        assert f'"{digit}"' in response.text or f"'{digit}'" in response.text or f'>{digit}<' in response.text
    # Check for operator buttons (+, -, *, /)
    for op in ["+", "-", "*", "/", "=", "C"]:
        assert op in response.text
    # Optionally verify the grid structure: ensure the page contains a 'grid' or 'calculator' class
    assert 'class="grid"' in response.text or 'class="calculator"' in response.text or 'class="keypad"' in response.text
