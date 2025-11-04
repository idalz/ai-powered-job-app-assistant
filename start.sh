#!/bin/bash

# Start script for JobMatch Assistant
# Starts both FastAPI backend and Streamlit frontend with auto-restart

echo "🚀 Starting JobMatch Assistant..."

# Convert Railway's DATABASE_URL format to SQLAlchemy psycopg format if needed
if [[ "$DATABASE_URL" == postgresql://* ]]; then
    export DATABASE_URL="${DATABASE_URL/postgresql:\/\//postgresql+psycopg:\/\/}"
    echo "✅ Converted DATABASE_URL to psycopg format"
fi

# Run database migrations first
echo "📦 Running database migrations..."
uv run alembic upgrade head

# Function to start FastAPI backend
start_backend() {
    echo "🔧 Starting FastAPI backend on port 8000..."
    uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
}

# Function to start Streamlit frontend
start_frontend() {
    echo "🎨 Starting Streamlit frontend on port 8501..."
    uv run streamlit run streamlit_app/main.py --server.address 0.0.0.0 --server.port 8501 &
    FRONTEND_PID=$!
}

# Function to cleanup on exit
cleanup() {
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

# Start backend
start_backend
sleep 5

# Start frontend
start_frontend

# Monitor both processes
while true; do
    # Check if backend is running
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo "⚠️ Backend crashed, restarting..."
        start_backend
        sleep 5
    fi

    # Check if frontend is running
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "⚠️ Frontend crashed, restarting..."
        start_frontend
        sleep 5
    fi

    # Wait before next check
    sleep 10
done
