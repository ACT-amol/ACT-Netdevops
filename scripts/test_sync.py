from extras.scripts import Script
class TestSync(Script):
    class Meta:
        name = "Connection Test"
        description = "Simple script to verify GitHub to NetBox sync"

    def run(self, data, commit):
        self.log_success("GitHub Sync is working perfectly!")
        self.log_info(f"Current System Version: v4.1.7")
        return "Success"
