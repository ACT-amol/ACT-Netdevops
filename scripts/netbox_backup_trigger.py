from extras.scripts import Script
import subprocess
import os

class BackupDevice(Script):
    class Meta:
        name = "Device Backup"
        description = "Triggers the Nornir backup from synced GitHub files"

    def run(self, data, commit):
        self.log_info("Starting Backup...")
        
<<<<<<< HEAD
        # 1. Find where NetBox put this script (the temporary GitHub sync folder)
        current_dir = os.path.dirname(os.path.realpath(__file__))
        
        # 2. Path to the shell script (assuming it's in the same folder in GitHub)
        script_path = os.path.join(current_dir, 'run_backup.sh')
=======
        # 1. Get the directory where THIS script is running
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.log_info(f"Searching for run_backup.sh in: {current_dir}")
>>>>>>> aea3d1d (Fix script path logic for NetBox Docker)

        # 2. Try to find run_backup.sh in the current folder or a 'scripts' subfolder
        script_path = ""
        possible_paths = [
            os.path.join(current_dir, 'run_backup.sh'),
            os.path.join(current_dir, 'scripts', 'run_backup.sh'),
            "/opt/netbox/netbox/scripts/automation/run_backup.sh" # Our permanent backup path
        ]

        for path in possible_paths:
            if os.path.exists(path):
                script_path = path
                break

        if not script_path:
            self.log_failure(f"CRITICAL: run_backup.sh not found. Checked: {possible_paths}")
            return

        self.log_info(f"Found script at: {script_path}")

        try:
<<<<<<< HEAD
            # 3. Check if file exists
            if not os.path.exists(script_path):
                self.log_failure(f"File not found at {script_path}. Ensure run_backup.sh is in your GitHub scripts folder.")
                return

            # 4. Give the script execution permissions (Docker temp folders often block this)
            subprocess.run(['chmod', '+x', script_path])

            # 5. Execute the bash script
            # We use 'bash' explicitly to avoid permission issues
=======
            # 3. Ensure the script is executable
            subprocess.run(['chmod', '+x', script_path], check=True)

            # 4. Execute the bash script
>>>>>>> aea3d1d (Fix script path logic for NetBox Docker)
            result = subprocess.run(['bash', script_path], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log_success(f"Backup Successful:\n{result.stdout}")
            else:
<<<<<<< HEAD
                self.log_failure(f"Script Error:\n{result.stderr}")
=======
                self.log_failure(f"Script Error (Exit Code {result.returncode}):\n{result.stderr}")
>>>>>>> aea3d1d (Fix script path logic for NetBox Docker)
                
        except Exception as e:
            self.log_failure(f"Execution Failed: {str(e)}")
