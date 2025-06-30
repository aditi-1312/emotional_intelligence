#!/bin/bash

# Emotional Intelligence Backend Startup Script with Custom Port
PORT=${1:-5001}

echo "🧠 Starting Emotional Intelligence Backend on port $PORT..."

# Kill any existing processes on the specified port
echo "🔄 Checking for existing processes on port $PORT..."
lsof -ti:$PORT | xargs kill -9 2>/dev/null || true

# Wait a moment for the port to be freed
sleep 2

# Change to backend directory and start the API with custom port
echo "🚀 Starting Flask API server on port $PORT..."
cd backend && PORT=$PORT python3 api.py 