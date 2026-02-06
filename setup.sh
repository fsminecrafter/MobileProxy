#!/bin/bash
set -e

echo "🥔 Setting up Le Potato appliance..."

sudo apt update
sudo apt install -y \
    python3 \
    python3-venv \
    python3-pip \
    openssh-server \
    tmux

# Enable SSH
sudo systemctl enable ssh
sudo systemctl start ssh

# Create venv
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python deps
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Start everything with:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Flask UI:  http://IP:8080/controlboard"
echo "Proxy:     configure browser to IP:8081"
