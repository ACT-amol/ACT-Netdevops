#!/bin/bash

# Move to the permanent volume directory
cd /opt/netbox/netbox/scripts/automation

echo "--- Starting Backup Pipeline ---"

# Use the venv we saw in your file list to run the python script
./venv/bin/python3 scripts/build_configs.py

echo "--- Backup Complete ---"
