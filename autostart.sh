#!/bin/bash

APP_DIR="/home/joel/lepotato-appliance"
VENV="$APP_DIR/venv"
APP="$APP_DIR/app.py"

cd "$APP_DIR" || exit 1

source "$VENV/bin/activate"

exec python "$APP"
