from extras.scripts import Script
import subprocess
import os

class BackupDevice(Script):
    class Meta:
        name = "Device Backup"
        description = "Triggers the Nornir backup from the verified automation path"

    def run(self, data, commit):
        self.log_info("Starting Backup Process...")
        
        # This is the EXACT path inside the Docker container that we verified earlier
        script_path = "/opt/netbox/netbox/scripts/automation/run_backup.sh"

        # Check if file exists before running
        if not os.path.exists(script_path):
            self.log_failure(f"CRITICAL: File not found at {script_path}")
            return

        self.log_info(f"Found script at: {script_path}. Executing via /bin/bash...")

        try:
            # We call /bin/bash explicitly. This avoids the "Permission Denied" 
            # error because we are asking bash to read the file rather than 
            # asking the file to run itself.
            result = subprocess.run(
                ['/bin/bash', script_path], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                self.log_success(f"Backup Successful:\n{result.stdout}")
            else:
                self.log_failure(f"Script Error (Exit Code {result.returncode}):\n{result.stderr}")
                
        except Exception as e:
            self.log_failure(f"Execution Failed: {str(e)}")
