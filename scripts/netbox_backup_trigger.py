from extras.scripts import Script
from django.utils.text import slugify
import subprocess

class BackupDevice(Script):
    class Meta:
        name = "Device Backup"
        description = "Triggers a Nornir backup and pushes to GitHub"

    def run(self, data, commit):
        # This executes your existing shell script from NetBox
        self.log_info("Starting Backup Pipeline...")
        try:
            result = subprocess.run(['/root/projects/ACT-Netdevops/run_backup.sh'], capture_output=True, text=True)
            self.log_success(f"Backup Complete: {result.stdout}")
        except Exception as e:
            self.log_failure(f"Error: {str(e)}")
