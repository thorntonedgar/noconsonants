#!/bin/bash
# Build script for production deployment

set -e

echo "Installing dependencies..."
pip install -r requirements.txt 

echo "Making migrations..."
python manage.py makemigrations


echo "Running migrations..."
python manage.py migrate --no-input

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Build complete!"

