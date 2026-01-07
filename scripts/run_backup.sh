#!/bin/bash

# 1. FORCE the script to go to your permanent Docker Volume folder
# This is where your venv, config.yaml, and inventory live.
PROJECT_ROOT="/opt/netbox/netbox/scripts/automation"

if [ ! -d "$PROJECT_ROOT" ]; then
    echo "ERROR: Project root $PROJECT_ROOT not found. Check Docker volume mount."
    exit 1
fi

cd "$PROJECT_ROOT"

echo "Current Directory: $(pwd)"

# 2. Run Nornir using the virtual environment in that folder
if [ -f "./venv/bin/python3" ]; then
    echo "Running Nornir build script..."
    ./venv/bin/python3 scripts/build_configs.py
else
    echo "ERROR: Virtual environment not found in $PROJECT_ROOT/venv"
    exit 1
fi

# 3. Handle GitHub Push
echo "Pushing rendered configs to GitHub..."
git add rendered/*.conf
git commit -m "Automated backup from NetBox $(date)"
git push origin main

echo "--- Pipeline Finished ---"

