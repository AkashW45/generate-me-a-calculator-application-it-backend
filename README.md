# Calculator API Service

A simple REST API calculator built with Python and FastAPI, supporting basic mathematical operations (addition, subtraction, multiplication, division, power) and a health check endpoint.

## Quick Start

### Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

4. Open http://localhost:8000 to access the static frontend (if included).

### Docker

Build and run:
```bash
docker build -t calculator-api .
docker run -p 8000:8000 calculator-api
```

## API Endpoints

| Method | Path       | Description                                  | Parameters       |
|--------|------------|----------------------------------------------|------------------|
| GET    | `/health`  | Liveness check (returns `{"status": "ok"}`) | None             |
| GET    | `/add`     | Addition                                     | `a` (float), `b` (float) |
| GET    | `/subtract`| Subtraction                                  | `a` (float), `b` (float) |
| GET    | `/multiply`| Multiplication                               | `a` (float), `b` (float) |
| GET    | `/divide`  | Division (returns 400 if b=0)                | `a` (float), `b` (float) |
| GET    | `/power`   | Exponentiation (a^b)                         | `a` (float), `b` (float) |

All endpoints return JSON with the result or an error.

## Example

```bash
curl "http://localhost:8000/add?a=3&b=4"
# {"result": 7.0}
```

## Testing

Run tests with pytest:
```bash
pytest tests/
```
