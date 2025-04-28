#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL is up!"

# Run Alembic migrations
echo "Running Alembic migrations..."
cd ..
alembic upgrade head
cd app

# Start the FastAPI app
echo "Starting FastAPI app..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
