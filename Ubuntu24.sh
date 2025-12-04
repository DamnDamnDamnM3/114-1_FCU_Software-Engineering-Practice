#!/bin/bash

clear

echo "Updating and upgrading packages..."
sudo apt update && sudo apt upgrade -y
echo "================================================"
echo "Done"
echo "================================================"

clear

echo "Installing MariaDB..."
sudo apt install -y mariadb-server
echo "================================================"
echo "Done"
echo "================================================"

clear

echo "Installing Python..."
sudo apt install -y python3 python3-pip python3-venv
echo "================================================"
echo "Done"
echo "================================================"

clear

echo "================================================"
echo "All done!"
echo "================================================"