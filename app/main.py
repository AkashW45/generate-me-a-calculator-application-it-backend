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
        <title>Calculator</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: Arial, sans-serif;
            }
            .calculator {
                background: white;
                border-radius: 15px;
                padding: 2rem;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                width: 100%;
                max-width: 400px;
            }
            .display {
                background: #f5f5f5;
                border-radius: 8px;
                padding: 1rem;
                margin-bottom: 1rem;
                text-align: right;
                min-height: 100px;
            }
            .display .expression {
                font-size: 1.2rem;
                color: #555;
                word-wrap: break-word;
                min-height: 1.5rem;
            }
            .display .result {
                font-size: 2.5rem;
                font-weight: bold;
                color: #000;
                margin-top: 0.5rem;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 8px;
            }
            .grid button {
                padding: 1rem;
                font-size: 1.5rem;
                border: none;
                border-radius: 8px;
                background: #e0e0e0;
                cursor: pointer;
                transition: background 0.2s;
            }
            .grid button:hover {
                background: #d0d0d0;
            }
            .grid button.operator {
                background: #f0a500;
                color: white;
            }
            .grid button.operator:hover {
                background: #d49400;
            }
            .grid button.equals {
                background: #007bff;
                color: white;
            }
            .grid button.equals:hover {
                background: #0069d9;
            }
            .grid button.clear {
                background: #dc3545;
                color: white;
            }
            .grid button.clear:hover {
                background: #c82333;
            }
            .grid button.func {
                background: #6c757d;
                color: white;
            }
            .grid button.func:hover {
                background: #5a6268;
            }
            .span-two {
                grid-column: span 2;
            }
        </style>
    </head>
    <body>
        <div class="calculator">
            <div class="display">
                <div id="expression" class="expression"></div>
                <div id="result" class="result">0</div>
            </div>
            <div class="grid">
                <button class="clear" onclick="clearAll()">C</button>
                <button class="func" onclick="toggleSign()">±</button>
                <button class="func" onclick="appendPercent()">%</button>
                <button class="operator" onclick="setOperator('/')">÷</button>
                <button onclick="appendDigit('7')">7</button>
                <button onclick="appendDigit('8')">8</button>
                <button onclick="appendDigit('9')">9</button>
                <button class="operator" onclick="setOperator('*')">×</button>
                <button onclick="appendDigit('4')">4</button>
                <button onclick="appendDigit('5')">5</button>
                <button onclick="appendDigit('6')">6</button>
                <button class="operator" onclick="setOperator('-')">−</button>
                <button onclick="appendDigit('1')">1</button>
                <button onclick="appendDigit('2')">2</button>
                <button onclick="appendDigit('3')">3</button>
                <button class="operator" onclick="setOperator('+')">+</button>
                <button class="span-two" onclick="appendDigit('0')">0</button>
                <button onclick="appendDot()">.</button>
                <button class="equals" onclick="calculate()">=</button>
            </div>
        </div>
        <script>
            let currentInput = '';
            let currentOperator = null;
            let firstOperand = null;
            let waitingForSecond = false;
            let expressionStr = '';
            let hasResult = false;
            let operatorMap = {
                '+': 'add',
                '-': 'subtract',
                '*': 'multiply',
                '/': 'divide',
                '^': 'power'
            };

            function updateDisplay() {
                document.getElementById('expression').textContent = expressionStr;
                const resultEl = document.getElementById('result');
                if (currentInput !== '' && !waitingForSecond) {
                    resultEl.textContent = currentInput;
                } else if (firstOperand !== null && waitingForSecond) {
                    resultEl.textContent = firstOperand;
                } else if (firstOperand !== null && currentOperator === null) {
                    resultEl.textContent = firstOperand;
                } else {
                    resultEl.textContent = '0';
                }
            }

            function appendDigit(digit) {
                if (hasResult) {
                    clearAll();
                }
                if (waitingForSecond) {
                    currentInput = digit;
                    waitingForSecond = false;
                } else {
                    currentInput = currentInput + digit;
                }
                rebuildExpression();
                updateDisplay();
            }

            function appendDot() {
                if (hasResult) {
                    clearAll();
                }
                if (waitingForSecond) {
                    currentInput = '0.';
                    waitingForSecond = false;
                } else {
                    if (currentInput.includes('.')) return;
                    if (currentInput === '') currentInput = '0';
                    currentInput = currentInput + '.';
                }
                rebuildExpression();
                updateDisplay();
            }

            function toggleSign() {
                if (hasResult) {
                    clearAll();
                }
                if (currentInput === '') return;
                if (currentInput.startsWith('-')) {
                    currentInput = currentInput.substring(1);
                } else {
                    currentInput = '-' + currentInput;
                }
                rebuildExpression();
                updateDisplay();
            }

            function appendPercent() {
                if (hasResult) {
                    clearAll();
                }
                if (currentInput === '') return;
                const num = parseFloat(currentInput);
                currentInput = String(num / 100);
                rebuildExpression();
                updateDisplay();
            }

            function setOperator(op) {
                if (hasResult) {
                    // Use result as first operand
                    firstOperand = parseFloat(document.getElementById('result').textContent);
                    currentInput = '';
                    waitingForSecond = true;
                    currentOperator = op;
                    hasResult = false;
                    expressionStr = firstOperand + ' ' + opSymbol(op);
                    updateDisplay();
                    return;
                }
                if (waitingForSecond) {
                    // Change operator
                    currentOperator = op;
                    expressionStr = firstOperand + ' ' + opSymbol(op);
                    updateDisplay();
                    return;
                }
                if (currentInput === '' && firstOperand === null) {
                    // Start with operator - default first operand to 0
                    firstOperand = 0;
                    currentOperator = op;
                    waitingForSecond = true;
                    expressionStr = firstOperand + ' ' + opSymbol(op);
                    updateDisplay();
                    return;
                }
                if (currentInput !== '') {
                    firstOperand = parseFloat(currentInput);
                    currentInput = '';
                    waitingForSecond = true;
                    currentOperator = op;
                    expressionStr = firstOperand + ' ' + opSymbol(op);
                    updateDisplay();
                    return;
                }
            }

            function opSymbol(op) {
                const map = {'+':'+', '-':'–', '*':'×', '/':'÷', '^':'^'};
                return map[op] || op;
            }

            function rebuildExpression() {
                if (firstOperand === null) {
                    expressionStr = currentInput;
                } else if (waitingForSecond) {
                    expressionStr = firstOperand + ' ' + opSymbol(currentOperator);
                } else {
                    expressionStr = firstOperand + ' ' + opSymbol(currentOperator) + ' ' + currentInput;
                }
            }

            async function calculate() {
                if (currentOperator === null || waitingForSecond || currentInput === '') {
                    return; // incomplete expression
                }
                const a = firstOperand;
                const b = parseFloat(currentInput);
                const op = operatorMap[currentOperator];
                if (!op) {
                    document.getElementById('result').textContent = 'Error';
                    return;
                }
                const url = `/${op}?a=${a}&b=${b}`;
                try {
                    const res = await fetch(url);
                    const data = await res.json();
                    if (res.ok) {
                        const result = data.result;
                        expressionStr = a + ' ' + opSymbol(currentOperator) + ' ' + b + ' =';
                        document.getElementById('expression').textContent = expressionStr;
                        document.getElementById('result').textContent = result;
                        hasResult = true;
                        firstOperand = result;
                        currentOperator = null;
                        currentInput = '';
                        waitingForSecond = false;
                    } else {
                        document.getElementById('result').textContent = 'Error: ' + (data.detail || 'Unknown');
                    }
                } catch(err) {
                    document.getElementById('result').textContent = 'Error';
                }
            }

            function clearAll() {
                currentInput = '';
                currentOperator = null;
                firstOperand = null;
                waitingForSecond = false;
                expressionStr = '';
                hasResult = false;
                updateDisplay();
                document.getElementById('expression').textContent = '';
                document.getElementById('result').textContent = '0';
            }
        </script>
    </body>
    </html>
    """

app.mount("/", StaticFiles(directory="static", html=True), name="static")
