from extras.scripts import Script, ObjectVar
from dcim.models import Device
import os

class HuaweiSafeScript(Script):
    device = ObjectVar(
        description="Select the Huawei switch to verify",
        queryset=Device.objects.filter(device_type__manufacturer__name__icontains="Huawei")
    )

    class Meta:
        name = "Huawei Config Verification"
        description = "Performs a ping test and confirms configuration status"

    def run(self, data, commit):
        target_device = data['device']
        
        # 1. Check if the device has an IP
        if not target_device.primary_ip:
            self.log_failure(f"❌ Device {target_device.name} has no Primary IP in NetBox.")
            return
        
        ip_addr = str(target_device.primary_ip.address.ip)
        self.log_info(f"Checking connectivity to {target_device.name} at {ip_addr}...")

        # 2. Perform a standard system ping (3 packets)
        # 'ping -c 3' works on Linux (the Docker container OS)
        response = os.system(f"ping -c 3 {ip_addr}")

        if response == 0:
            self.log_success(f"✅ Ping to {ip_addr} successful.")
            
            # 3. Display the configuration message you requested
            self.log_success("✅ Configuration has been implemented successfully.")
            self.log_info("Note: This was a simulation. No changes were made to the hardware.")
        else:
            self.log_failure(f"❌ Ping to {ip_addr} failed. Switch might be offline.")

        return "Process Finished"
