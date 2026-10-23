#!/usr/bin/env bash
# Convenience launcher for macOS/Linux.
set -e

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -q -r requirements.txt

if [ ! -f ".env" ]; then
  cp .env.example .env
fi

echo "Starting HR Multi-Agent Assistant on http://127.0.0.1:8000"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
