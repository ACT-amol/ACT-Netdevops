from extras.scripts import Script, ObjectVar
from dcim.models import Device, Interface

class InterfaceStatusScript(Script):
    device = ObjectVar(
        description="Select a device to check interface status",
        queryset=Device.objects.all()
    )

    class Meta:
        name = "Device Interface Check"
        description = "Displays the status of interfaces from the NetBox database"

    def run(self, data, commit):
        target_device = data['device']
        
        # Pull all interfaces for the selected device from the database
        interfaces = Interface.objects.filter(device=target_device)
        
        self.log_info(f"Checking interfaces for: {target_device.name}")
        
        if not interfaces.exists():
            self.log_warning("No interfaces found for this device in NetBox.")
            return

        for iface in interfaces:
            # Check if the interface is marked as active/enabled in NetBox
            status = "UP/ENABLED" if iface.enabled else "DOWN/DISABLED"
            
            if iface.enabled:
                self.log_success(f"Interface {iface.name}: {status}")
            else:
                self.log_failure(f"Interface {iface.name}: {status}")

        self.log_success("✅ Interface status check completed successfully!")
        return "Success"
