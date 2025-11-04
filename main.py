#!/usr/bin/env python3
"""
Main entry point for JobMatch Assistant on Railway
Starts both FastAPI backend and Streamlit frontend
"""
import os
import subprocess
import sys
import time
import signal
from typing import Optional

# Global process references
backend_process: Optional[subprocess.Popen] = None
frontend_process: Optional[subprocess.Popen] = None


def convert_database_url():
    """Convert Railway's DATABASE_URL to SQLAlchemy psycopg format"""
    db_url = os.environ.get("DATABASE_URL", "")
    if db_url.startswith("postgresql://"):
        new_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)
        os.environ["DATABASE_URL"] = new_url
        print("✅ Converted DATABASE_URL to psycopg format")


def run_migrations():
    """Run database migrations"""
    print("📦 Running database migrations...")
    try:
        subprocess.run(
            ["uv", "run", "alembic", "upgrade", "head"],
            check=True,
            capture_output=False
        )
        print("✅ Migrations completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)


def start_backend():
    """Start FastAPI backend on port 8000"""
    global backend_process
    print("🔧 Starting FastAPI backend on port 8000...")
    backend_process = subprocess.Popen(
        ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    return backend_process


def start_frontend():
    """Start Streamlit frontend on port 8501"""
    global frontend_process
    print("🎨 Starting Streamlit frontend on port 8501...")
    frontend_process = subprocess.Popen(
        ["uv", "run", "streamlit", "run", "streamlit_app/main.py",
         "--server.address", "0.0.0.0", "--server.port", "8501"],
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    return frontend_process


def cleanup(signum=None, frame=None):
    """Cleanup handler for graceful shutdown"""
    print("\n🛑 Shutting down services...")
    if backend_process:
        backend_process.terminate()
        backend_process.wait(timeout=5)
    if frontend_process:
        frontend_process.terminate()
        frontend_process.wait(timeout=5)
    sys.exit(0)


def monitor_processes():
    """Monitor both processes and restart if they crash"""
    global backend_process, frontend_process

    while True:
        # Check if backend is running
        if backend_process and backend_process.poll() is not None:
            print("⚠️ Backend crashed, restarting...")
            backend_process = start_backend()
            time.sleep(5)

        # Check if frontend is running
        if frontend_process and frontend_process.poll() is not None:
            print("⚠️ Frontend crashed, restarting...")
            frontend_process = start_frontend()
            time.sleep(5)

        # Wait before next check
        time.sleep(10)


if __name__ == "__main__":
    print("🚀 Starting JobMatch Assistant...")

    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)

    # Convert DATABASE_URL format if needed
    convert_database_url()

    # Run database migrations
    run_migrations()

    # Start backend
    start_backend()
    time.sleep(5)  # Give backend time to start

    # Start frontend
    start_frontend()

    # Monitor both processes
    try:
        monitor_processes()
    except KeyboardInterrupt:
        cleanup()
