#!/bin/bash

# Vendor Management System - Frontend Startup Script

echo "Starting Vendor Management Frontend..."

# Navigate to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Create environment file if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "Creating environment file..."
    echo "REACT_APP_API_URL=http://localhost:8000/api" > .env.local
fi

# Start React development server
echo "Starting React development server..."
echo "Frontend will be available at: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the server"

npm start
