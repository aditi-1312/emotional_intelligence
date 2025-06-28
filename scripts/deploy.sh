#!/bin/bash

# Emotional Intelligence Mood Tracker - Deployment Script
# This script helps set up and deploy the application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python() {
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_status "Python version: $PYTHON_VERSION"
        return 0
    else
        print_error "Python 3 is not installed. Please install Python 3.8+"
        return 1
    fi
}

# Function to check Node.js version
check_node() {
    if command_exists node; then
        NODE_VERSION=$(node --version)
        print_status "Node.js version: $NODE_VERSION"
        return 0
    else
        print_error "Node.js is not installed. Please install Node.js 14+"
        return 1
    fi
}

# Function to install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    if command_exists pip3; then
        pip3 install -r requirements.txt
        print_success "Python dependencies installed successfully"
    else
        print_error "pip3 is not available. Please install pip"
        return 1
    fi
}

# Function to install Node.js dependencies
install_node_deps() {
    print_status "Installing Node.js dependencies..."
    
    if command_exists npm; then
        cd frontend
        npm install
        cd ..
        print_success "Node.js dependencies installed successfully"
    else
        print_error "npm is not available. Please install Node.js"
        return 1
    fi
}

# Function to setup environment
setup_env() {
    print_status "Setting up environment..."
    
    if [ ! -f config.env ]; then
        if [ -f config.env.example ]; then
            cp config.env.example config.env
            print_warning "Created config.env from template. Please edit it with your settings."
        else
            print_error "config.env.example not found"
            return 1
        fi
    else
        print_status "config.env already exists"
    fi
    
    # Create necessary directories
    mkdir -p data_and_models/logs
    mkdir -p data_and_models/output
    
    print_success "Environment setup completed"
}

# Function to start development servers
start_dev() {
    print_status "Starting development servers..."
    
    # Check if ports are available
    if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
        print_warning "Port 5001 is already in use. Please stop the existing process."
        return 1
    fi
    
    if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
        print_warning "Port 3000 is already in use. Please stop the existing process."
        return 1
    fi
    
    # Start backend in background
    print_status "Starting Flask API server on port 5001..."
    PORT=5001 python3 backend/api.py &
    BACKEND_PID=$!
    
    # Wait a moment for backend to start
    sleep 3
    
    # Start frontend
    print_status "Starting React development server on port 3000..."
    cd frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
    
    print_success "Development servers started!"
    print_status "Backend API: http://localhost:5001"
    print_status "Frontend App: http://localhost:3000"
    print_status "Press Ctrl+C to stop both servers"
    
    # Wait for user to stop
    wait
}

# Function to stop development servers
stop_dev() {
    print_status "Stopping development servers..."
    
    # Kill processes on ports 5001 and 3000
    pkill -f "python3 backend/api.py" || true
    pkill -f "react-scripts start" || true
    
    print_success "Development servers stopped"
}

# Function to build for production
build_prod() {
    print_status "Building for production..."
    
    # Build frontend
    cd frontend
    npm run build
    cd ..
    
    print_success "Production build completed"
}

# Function to run tests
run_tests() {
    print_status "Running tests..."
    
    # Run backend tests
    if [ -f backend/test_system.py ]; then
        python3 backend/test_system.py
    fi
    
    # Run frontend tests
    cd frontend
    npm test -- --watchAll=false
    cd ..
    
    print_success "Tests completed"
}

# Function to show help
show_help() {
    echo "Emotional Intelligence Mood Tracker - Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup     - Install dependencies and setup environment"
    echo "  dev       - Start development servers"
    echo "  stop      - Stop development servers"
    echo "  build     - Build for production"
    echo "  test      - Run tests"
    echo "  check     - Check system requirements"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup  # Install dependencies"
    echo "  $0 dev    # Start development servers"
    echo "  $0 stop   # Stop development servers"
}

# Function to check system requirements
check_system() {
    print_status "Checking system requirements..."
    
    check_python
    check_node
    
    print_success "System requirements check completed"
}

# Main script logic
case "${1:-help}" in
    setup)
        print_status "Setting up Emotional Intelligence Mood Tracker..."
        check_system
        install_python_deps
        install_node_deps
        setup_env
        print_success "Setup completed successfully!"
        ;;
    dev)
        start_dev
        ;;
    stop)
        stop_dev
        ;;
    build)
        build_prod
        ;;
    test)
        run_tests
        ;;
    check)
        check_system
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac 