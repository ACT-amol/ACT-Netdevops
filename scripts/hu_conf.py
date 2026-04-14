from extras.scripts import Script, ObjectVar, TextVar, PasswordVar
from dcim.models import Device
try:
    from netmiko import ConnectHandler
    NETMIKO_READY = True
except ImportError:
    NETMIKO_READY = False

class HuaweiConfigScript(Script):
    # Instead of typing an IP, you select a device from your NetBox list
    device = ObjectVar(
        description="Select the Huawei switch to configure",
        queryset=Device.objects.filter(device_type__manufacturer__name="Huawei")
    )
    username = StringVar(label="SSH Username", default="venkatasatya.teja")
    password = PasswordVar(label="SSH Password", default="Login@999")
    commands = TextVar(label="Configuration Commands")

    class Meta:
        name = "Huawei Configuration Tool (Auto-IP)"
        description = "Pulls IP automatically from NetBox device records"

    def run(self, data, commit):
        if not NETMIKO_READY:
            self.log_failure("Netmiko not installed in worker container.")
            return

        # Get the IP address from the device object you selected in the UI
        target_device = data['device']
        if not target_device.primary_ip:
            self.log_failure(f"Device {target_device.name} has no Primary IP assigned in NetBox!")
            return
            
        # Clean the IP (removes the /mask like /24)
        ip_address = str(target_device.primary_ip.address.ip)

        huawei_device = {
            'device_type': 'huawei',
            'host': ip_address,
            'username': data['username'],
            'password': data['password'],
            'port': 22,
            'conn_timeout': 15,
        }

        self.log_info(f"Connecting to {target_device.name} at {ip_address}...")
        
        try:
            with ConnectHandler(**huawei_device) as net_connect:
                self.log_success(f"Connected to {target_device.name}")
                output = net_connect.send_config_set(data['commands'].strip().splitlines())
                self.log_info(output)
                self.log_success("Done.")
        except Exception as e:
            self.log_failure(f"Failed: {str(e)}")

        return "Finished"
