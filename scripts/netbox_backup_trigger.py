from extras.scripts import Script
import subprocess

class BackupDevice(Script):
    class Meta:
        name = "Device Backup"
        description = "Triggers the Nornir backup"

    def run(self, data, commit):
        self.log_info("Starting Backup...")
        # Since NetBox is in Docker, we attempt to run the command.
        # Note: This will only work if the shell script is accessible inside the container.
        try:
            # TRY THIS FIRST: Use the path where NetBox stores synced data scripts
            result = subprocess.run(['bash', '/opt/netbox/netbox/scripts/run_backup.sh'], capture_output=True, text=True)
            self.log_success(f"Output: {result.stdout}")
        except Exception as e:
            self.log_failure(f"Error: {str(e)}")
