#!/bin/bash

echo "🔄 Restarting Emotional Intelligence Backend..."

# Kill any existing backend processes
echo "Killing existing backend processes..."
pkill -f "python3 api.py" 2>/dev/null
lsof -ti:5001 | xargs kill -9 2>/dev/null
lsof -ti:5002 | xargs kill -9 2>/dev/null

# Wait a moment
sleep 2

# Start backend on port 5002
echo "Starting backend on port 5002..."
cd backend
PORT=5002 python3 api.py &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 5

# Test health endpoint
echo "Testing backend health..."
if curl -s http://localhost:5002/health > /dev/null; then
    echo "✅ Backend is running successfully!"
    echo "🌐 API available at: http://localhost:5002"
    echo "📊 Health check: http://localhost:5002/health"
    echo ""
    echo "To stop the backend, run: kill $BACKEND_PID"
else
    echo "❌ Backend failed to start or is not responding"
    exit 1
fi 