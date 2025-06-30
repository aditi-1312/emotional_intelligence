#!/bin/bash

# Emotional Intelligence Frontend Startup Script
echo "🎨 Starting Emotional Intelligence Frontend..."

# Check if port 3000 is in use
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 3000 is in use. Starting on port 3001..."
    cd frontend && PORT=3001 npm start
else
    echo "🚀 Starting React app on port 3000..."
    cd frontend && npm start
fi 