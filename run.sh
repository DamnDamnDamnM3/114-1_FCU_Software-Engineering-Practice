#!/bin/bash

clear

echo "Activating virtual environment..."
source venv/bin/activate
echo "================================================"
echo "Done"
echo "================================================"

clear

echo "Running application..."
python3 src/app.py
echo "================================================"
echo "Done"
echo "================================================"