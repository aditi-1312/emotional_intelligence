#!/bin/bash

# Emotional Intelligence App Startup Script
echo "🧠🎨 Starting Emotional Intelligence App..."

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to kill process on port
kill_port() {
    local port=$1
    echo "🔄 Killing process on port $port..."
    lsof -ti:$port | xargs kill -9 2>/dev/null || true
    sleep 2
}

# Check and handle backend port
if check_port 5001; then
    echo "⚠️  Port 5001 is in use. Using port 5002 for backend..."
    BACKEND_PORT=5002
    kill_port 5002
else
    BACKEND_PORT=5001
fi

# Check and handle frontend port
if check_port 3000; then
    echo "⚠️  Port 3000 is in use. Using port 3001 for frontend..."
    FRONTEND_PORT=3001
else
    FRONTEND_PORT=3000
fi

echo "🚀 Starting backend on port $BACKEND_PORT..."
cd backend && PORT=$BACKEND_PORT python3 api.py &
BACKEND_PID=$!

echo "⏳ Waiting for backend to start..."
sleep 5

echo "🎨 Starting frontend on port $FRONTEND_PORT..."
cd frontend && PORT=$FRONTEND_PORT npm start &
FRONTEND_PID=$!

echo "✅ Both services started!"
echo "📱 Backend: http://localhost:$BACKEND_PORT"
echo "🎨 Frontend: http://localhost:$FRONTEND_PORT"
echo "⏹️  Press Ctrl+C to stop both services"

# Wait for user to stop
wait 