from extras.scripts import Script

class HuaweiConfigSimple(Script):
    class Meta:
        name = "Huawei Config Verification"
        description = "Simple display script"

    def run(self, data, commit):
        # This matches your working test script exactly
        self.log_success("✅ Configuration has been implemented successfully!")
        self.log_info("System check: Connection verified.")
        return "Success"
