from extras.scripts import Script
import subprocess
import os

class BackupDevice(Script):
    class Meta:
        name = "Device Backup"
        description = "Triggers the Nornir backup from synced GitHub files"

    def run(self, data, commit):
        self.log_info("Starting Backup...")
        
        # 1. Find where NetBox put this script (the temporary GitHub sync folder)
        current_dir = os.path.dirname(os.path.realpath(__file__))
        
        # 2. Path to the shell script (assuming it's in the same folder in GitHub)
        script_path = os.path.join(current_dir, 'run_backup.sh')

        self.log_info(f"Looking for shell script at: {script_path}")

        try:
            # 3. Check if file exists
            if not os.path.exists(script_path):
                self.log_failure(f"File not found at {script_path}. Ensure run_backup.sh is in your GitHub scripts folder.")
                return

            # 4. Give the script execution permissions (Docker temp folders often block this)
            subprocess.run(['chmod', '+x', script_path])

            # 5. Execute the bash script
            # We use 'bash' explicitly to avoid permission issues
            result = subprocess.run(['bash', script_path], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log_success(f"Backup Successful:\n{result.stdout}")
            else:
                self.log_failure(f"Script Error:\n{result.stderr}")
                
        except Exception as e:
            self.log_failure(f"Execution Failed: {str(e)}")
