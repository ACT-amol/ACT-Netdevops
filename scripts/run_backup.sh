#!/bin/bash

# 1. Get the directory where THIS script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 2. Navigate to the root of the project (one level up from /scripts)
cd "$SCRIPT_DIR/.."

echo "--- Starting NetDevOps Backup Pipeline ---"
echo "Current Directory: $(pwd)"

# 3. Check if we are inside the Docker container or on the Host
if [ -f "/opt/netbox/venv/bin/python3" ]; then
    echo "Running inside NetBox Docker container..."
    # If you successfully ran the pip install command earlier:
    /opt/netbox/venv/bin/python3 scripts/build_configs.py
else
    echo "Running on Host machine..."
    # Path to your local virtual environment on the act-nms-dev server
    source venv/bin/activate
    python3 scripts/build_configs.py
fi

# 4. Optional: Handle Git pushes if needed (usually handled by the python script)
# git add .
# git commit -m "Automated backup from NetBox"
# git push origin main

echo "--- Pipeline Execution Finished ---"
