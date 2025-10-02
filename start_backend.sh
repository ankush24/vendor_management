#!/bin/bash

# Vendor Management System - Backend Startup Script

echo "Starting Vendor Management Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check if PostgreSQL is running
echo "Checking PostgreSQL connection..."
python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='localhost',
        database='vendor_management',
        user='postgres',
        password='password'
    )
    conn.close()
    print('PostgreSQL connection successful')
except Exception as e:
    print(f'PostgreSQL connection failed: {e}')
    print('Please ensure PostgreSQL is running and database is created')
    exit(1)
"

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser (if not exists)..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: username=admin, password=admin123')
else:
    print('Superuser already exists')
"

# Start Celery worker in background
echo "Starting Celery worker..."
celery -A vendor_management_backend worker --loglevel=info &
CELERY_PID=$!

# Start Celery beat in background
echo "Starting Celery beat..."
celery -A vendor_management_backend beat --loglevel=info &
BEAT_PID=$!

# Start Django development server
echo "Starting Django development server..."
echo "Backend will be available at: http://localhost:8000"
echo "Admin interface: http://localhost:8000/admin"
echo "API documentation: http://localhost:8000/swagger/"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup background processes
cleanup() {
    echo "Stopping services..."
    kill $CELERY_PID 2>/dev/null
    kill $BEAT_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Start Django server
python manage.py runserver

# Cleanup on exit
cleanup
