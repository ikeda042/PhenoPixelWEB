#!/bin/bash

echo "Creating Python virtual environment..."
python3 -m venv venv
echo "Python virtual environment created."

echo "Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated."

echo "Pulling latest code from main branch..."
git pull origin main
echo "Latest code pulled."

echo "Moving to frontend directory..."
cd frontend 
echo "Moved to frontend directory."

echo "Starting frontend..."
npm start &
echo "Frontend started."

echo "Moving to backend directory..."
cd ..
cd backend
echo "Moved to backend directory."

echo "Starting backend..."
python router.py
echo "Backend started."
