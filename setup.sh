#!/bin/bash

# Vendor Management System - Complete Setup Script

echo "=========================================="
echo "Vendor Management System Setup"
echo "=========================================="

# Check if PostgreSQL is installed and running
echo "Checking PostgreSQL..."
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL is not installed. Please install PostgreSQL first."
    echo "On macOS: brew install postgresql"
    echo "On Ubuntu: sudo apt-get install postgresql postgresql-contrib"
    exit 1
fi

# Check if Redis is installed and running
echo "Checking Redis..."
if ! command -v redis-server &> /dev/null; then
    echo "Redis is not installed. Please install Redis first."
    echo "On macOS: brew install redis"
    echo "On Ubuntu: sudo apt-get install redis-server"
    exit 1
fi

# Start Redis if not running
if ! pgrep -x "redis-server" > /dev/null; then
    echo "Starting Redis server..."
    redis-server --daemonize yes
fi

# Create PostgreSQL database
echo "Creating PostgreSQL database..."
sudo -u postgres psql -c "CREATE DATABASE vendor_management;" 2>/dev/null || echo "Database may already exist"
sudo -u postgres psql -c "CREATE USER postgres WITH PASSWORD 'password';" 2>/dev/null || echo "User may already exist"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE vendor_management TO postgres;" 2>/dev/null || echo "Privileges may already be granted"

# Create environment file
echo "Creating environment configuration..."
cat > .env << EOF
# Database Configuration
DB_NAME=vendor_management
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Django Configuration
SECRET_KEY=django-insecure-+ei)y*okokqgi4&=$g6ao#%yv2li@sa0979b4@e@40v@74&mb@
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@vendor-management.com

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
EOF

# Setup Python backend
echo "Setting up Python backend..."
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Run Django migrations
echo "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: username=admin, password=admin123')
else:
    print('Superuser already exists')
"

# Setup Node.js frontend
echo "Setting up Node.js frontend..."
cd frontend
npm install

# Create frontend environment file
echo "Creating frontend environment configuration..."
cat > .env.local << EOF
REACT_APP_API_URL=http://localhost:8000/api
EOF

cd ..

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To start the application:"
echo "1. Backend: ./start_backend.sh"
echo "2. Frontend: ./start_frontend.sh (in a new terminal)"
echo ""
echo "Access points:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000/api"
echo "- Admin: http://localhost:8000/admin"
echo "- API Docs: http://localhost:8000/swagger/"
echo ""
echo "Default login credentials:"
echo "- Username: admin"
echo "- Password: admin123"
echo ""
echo "Make sure to update email settings in .env file for notifications!"
