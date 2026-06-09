from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
import math
from fastapi.responses import HTMLResponse

app = FastAPI(title="Calculator API", version="1.0.0")

# ------------------- API Endpoints -------------------

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/add")
async def add(a: float = Query(...), b: float = Query(...)):
    return {"result": a + b}

@app.get("/subtract")
async def subtract(a: float = Query(...), b: float = Query(...)):
    return {"result": a - b}

@app.get("/multiply")
async def multiply(a: float = Query(...), b: float = Query(...)):
    return {"result": a * b}

@app.get("/divide")
async def divide(a: float = Query(...), b: float = Query(...)):
    if b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed")
    return {"result": a / b}

@app.get("/power")
async def power(a: float = Query(...), b: float = Query(...)):
    return {"result": math.pow(a, b)}

# ------------------- Static Frontend -------------------
# Must be mounted AFTER API routes to avoid route conflicts
@app.get("/calculator", response_class=HTMLResponse)
async def calculator_ui():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Modern Calculator</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .calculator-card { background: white; border-radius: 15px; padding: 2rem; box-shadow: 0 10px 40px rgba(0,0,0,0.2); width: 100%; max-width: 500px; }
            .result-box { font-size: 2rem; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="calculator-card">
            <h2 class="text-center mb-4">Calculator</h2>
            <div class="mb-3">
                <label class="form-label">First Number</label>
                <input type="number" id="a" class="form-control" step="any">
            </div>
            <div class="mb-3">
                <label class="form-label">Second Number</label>
                <input type="number" id="b" class="form-control" step="any">
            </div>
            <div class="mb-3">
                <label class="form-label">Operation</label>
                <select id="op" class="form-select">
                    <option value="add">+</option>
                    <option value="subtract">−</option>
                    <option value="multiply">×</option>
                    <option value="divide">÷</option>
                    <option value="power">^</option>
                </select>
            </div>
            <button class="btn btn-primary w-100" onclick="calculate()">Calculate</button>
            <div id="result" class="result-box text-center mt-3"></div>
        </div>
        <script>
            async function calculate() {
                const a = document.getElementById('a').value;
                const b = document.getElementById('b').value;
                const op = document.getElementById('op').value;
                const url = `/${op}?a=${a}&b=${b}`;
                try {
                    const res = await fetch(url);
                    const data = await res.json();
                    document.getElementById('result').innerText = data.result;
                } catch(err) {
                    document.getElementById('result').innerText = 'Error';
                }
            }
        </script>
    </body>
    </html>
    """

app.mount("/", StaticFiles(directory="static", html=True), name="static")
