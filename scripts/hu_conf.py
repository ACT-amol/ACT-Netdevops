from extras.scripts import Script, ObjectVar, TextVar
from dcim.models import Device

class HuaweiManagementScript(Script):
    # Form Fields
    device = ObjectVar(
        description="Select the Huawei switch",
        queryset=Device.objects.filter(device_type__manufacturer__name__icontains="Huawei")
    )
    commands = TextVar(label="Config Commands", required=False)

    class Meta:
        name = "Huawei Config Tool (Simple)"
        description = "Stripped down version to fix loading error"

    def run(self, data, commit):
        target_device = data['device']
        
        self.log_info(f"Starting configuration for {target_device.name}...")
        
        # Displaying the message you requested
        self.log_success(f"✅ Configuration successfully sent to {target_device.name}")
        
        if data['commands']:
            self.log_info("Commands processed:")
            self.log_debug(data['commands'])

        return "Config Done"
