#!/bin/bash
# Move to the project directory inside the container
cd /opt/netbox/netbox/scripts/automation

# Use the virtual environment's python to run the build
./venv/bin/python3 scripts/build_configs.py

# Optional: Add your git commands here later
