#!/bin/bash

# 1. FORCE the script to go to the permanent Docker volume we created
PROJECT_ROOT="/opt/netbox/netbox/scripts/automation"
cd "$PROJECT_ROOT"

echo "--- Starting NetDevOps Backup Pipeline ---"
echo "Current Working Directory: $(pwd)"

# 2. Use the virtual environment inside THAT folder
if [ -f "./venv/bin/python3" ]; then
    echo "Using project virtual environment..."
    ./venv/bin/python3 scripts/build_configs.py
else
    echo "ERROR: Virtual environment not found in $PROJECT_ROOT/venv"
    exit 1
fi

echo "--- Pipeline Execution Finished ---"
