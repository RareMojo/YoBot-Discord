#!/bin/sh

echo "Setting up YoBot..."

echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip --progress-bar on

echo "Installing dependencies..."
pip install -r requirements.txt --progress-bar on

echo "Starting YoBot..."
python src/main.py
