from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
import math

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
app.mount("/", StaticFiles(directory="static", html=True), name="static")
