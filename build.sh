#!/bin/bash
# Build script for production deployment

set -e

echo "Installing uv..."
pip install uv

echo "Installing dependencies with uv..."
uv pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate --no-input

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Build complete!"

