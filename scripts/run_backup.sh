#!/bin/bash
# Navigate to the project directory
cd /root/projects/ACT-Netdevops

# Activate the virtual environment
source venv/bin/activate

# Run your Nornir backup script (Update the name if yours is different)
python3 scripts/build_configs.py

# Push the changes to GitHub
git add .
git commit -m "Automated backup from NetBox Script"
git push origin main
