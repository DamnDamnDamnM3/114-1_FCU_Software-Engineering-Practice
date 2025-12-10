#!/bin/bash

# sudo apt update && sudo apt upgrade -y

# sudo apt install -y python3 python3-pip python3-venv

clear

echo "Creating virtual environment..."
python3 -m venv venv
echo "================================================"
echo "Done"
echo "================================================"

clear

echo "Activating virtual environment..."
source venv/bin/activate
echo "================================================"
echo "Done"
echo "================================================"

clear

echo "Installing requirements..."
pip install -r src/requirements.txt
echo "================================================"
echo "Done"
echo "================================================"

clear

echo "================================================"
echo "All done!"
echo "================================================"