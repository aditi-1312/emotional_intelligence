#!/bin/bash

# Emotional Intelligence Backend Startup Script
echo "🧠 Starting Emotional Intelligence Backend..."

# Kill any existing processes on port 5001
echo "🔄 Checking for existing processes on port 5001..."
lsof -ti:5001 | xargs kill -9 2>/dev/null || true

# Wait a moment for the port to be freed
sleep 2

# Change to backend directory and start the API
echo "🚀 Starting Flask API server..."
cd backend && python3 api.py 