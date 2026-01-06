from extras.scripts import Script
import subprocess
import os

class BackupDevice(Script):
    class Meta:
        name = "Device Backup"
        description = "Triggers the Nornir backup from synced GitHub files"
def run(self, data, commit):
        self.log_info("Starting Backup...")
        
        # Get the directory where THIS Python script is located
        current_dir = os.path.dirname(os.path.realpath(__file__))
        
        # Look for run_backup.sh in that SAME folder
        script_path = os.path.join(current_dir, 'run_backup.sh')

        self.log_info(f"Looking for shell script at: {script_path}")
        # ... rest of your code ...

        try:
            # Check if file exists before running
            if not os.path.exists(script_path):
                self.log_failure(f"File not found at {script_path}. Check your GitHub folder structure.")
                return

            # Execute the bash script
            result = subprocess.run(['bash', script_path], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log_success(f"Backup Successful: {result.stdout}")
            else:
                self.log_failure(f"Script Error: {result.stderr}")
        except Exception as e:
            self.log_failure(f"Execution Failed: {str(e)}")
