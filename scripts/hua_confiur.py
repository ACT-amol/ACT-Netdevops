from extras.scripts import Script

class HuaweiSimpleScript(Script):
    class Meta:
        name = "Huawei Config Simple"
        description = "Minimalist version to force clear errors"

    def run(self, data, commit):
        self.log_success("✅ Configuration push simulated and Done!")
        return "Finished"
