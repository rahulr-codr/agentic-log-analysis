#!/bin/bash

# Ensure we're in the right directory
cd "$(dirname "$0")"

# Check if virtual environment exists, if not create it
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies if needed
if [ ! -f ".venv/installed" ]; then
    echo "Installing dependencies..."
    uv pip install fastapi "uvicorn[standard]" httpx pydantic pydantic-settings python-dotenv
    touch .venv/installed
fi

# Run the application
echo "Starting the application..."
PYTHONPATH=$PYTHONPATH:. uvicorn lookup_service.main:app --reload --host 0.0.0.0 --port 8000 