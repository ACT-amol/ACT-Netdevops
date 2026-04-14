from extras.scripts import Script, ObjectVar, TextVar, PasswordVar
from dcim.models import Device

class HuaweiManagementScript(Script):
    # Form Fields
    device = ObjectVar(
        description="Select the Huawei switch",
        queryset=Device.objects.filter(device_type__manufacturer__name__icontains="Huawei")
    )
    username = StringVar(label="SSH Username", default="venkatasatya.teja")
    password = PasswordVar(label="SSH Password", default="Login@999")
    commands = TextVar(label="Config Commands", required=False)

    class Meta:
        name = "Huawei Backup & Config Tool"
        description = "Simple loader - No blocking imports"

    def run(self, data, commit):
        # We import INSIDE the run function so the UI doesn't crash on load
        try:
            from netmiko import ConnectHandler
        except ImportError:
            self.log_failure("ERROR: 'netmiko' is not installed in the Docker Worker.")
            self.log_info("Run: docker exec -u root netbox-docker-netbox-worker-1 pip install netmiko")
            return

        target_device = data['device']
        if not target_device.primary_ip:
            self.log_failure(f"Device {target_device.name} has no Primary IP.")
            return
        
        ip_addr = str(target_device.primary_ip.address.ip)

        # Connection logic
        huawei_params = {
            'device_type': 'huawei',
            'host': ip_addr,
            'username': data['username'],
            'password': data['password'],
            'conn_timeout': 15,
        }

        try:
            self.log_info(f"Connecting to {ip_addr}...")
            with ConnectHandler(**huawei_params) as net_connect:
                self.log_success("Connected!")
                
                if data['commands']:
                    output = net_connect.send_config_set(data['commands'].splitlines())
                    self.log_info(output)
                    self.log_success("Config Pushed.")
                else:
                    output = net_connect.send_command("display current-configuration")
                    self.log_info("Backup captured (see log).")
                    
        except Exception as e:
            self.log_failure(f"Connection Failed: {str(e)}")

        return "Finished"
