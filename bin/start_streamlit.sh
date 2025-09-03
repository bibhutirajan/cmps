#!/bin/bash

# Start Streamlit application for local development
echo "Starting CMPS Streamlit Application..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Start Streamlit
echo "Starting Streamlit on http://localhost:8501"
streamlit run app.py --server.port 8501

