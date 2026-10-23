@echo off
IF NOT EXIST .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat
pip install -q -r requirements.txt

IF NOT EXIST .env (
    copy .env.example .env
)

echo Starting HR Multi-Agent Assistant on http://127.0.0.1:8000
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
