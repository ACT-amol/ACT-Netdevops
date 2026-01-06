from extras.scripts import Script
import subprocess
import os

class BackupDevice(Script):
    class Meta:
        name = "Device Backup"
        description = "Triggers the Nornir backup from the synced GitHub files"

    def run(self, data, commit):
        self.log_info("Starting Backup...")
        
        # Get the directory where THIS script is currently running
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # Find the shell script in the same folder
        script_path = os.path.join(current_dir, 'run_backup.sh')

        self.log_info(f"Running script at: {script_path}")

        try:
            # Execute the bash script
            result = subprocess.run(['bash', script_path], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log_success(f"Backup Successful: {result.stdout}")
            else:
                self.log_failure(f"Script Error: {result.stderr}")
        except Exception as e:
            self.log_failure(f"Execution Failed: {str(e)}")
