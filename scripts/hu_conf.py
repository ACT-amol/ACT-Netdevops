from extras.scripts import Script, ObjectVar, TextVar, PasswordVar, BooleanVar
from dcim.models import Device
import datetime

# --- ERROR PREVENTION BLOCK ---
try:
    from netmiko import ConnectHandler
    NETMIKO_LOADED = True
except ImportError:
    NETMIKO_LOADED = False

class HuaweiManagementScript(Script):
    device = ObjectVar(
        description="Select the Huawei switch",
        queryset=Device.objects.filter(device_type__manufacturer__name__icontains="Huawei")
    )
    username = StringVar(label="SSH Username", default="venkatasatya.teja")
    password = PasswordVar(label="SSH Password", default="Login@999")
    
    do_backup = BooleanVar(label="Run Backup", default=True, description="Capture 'display current-configuration'")
    commands = TextVar(label="Push Config Commands", required=False, description="Enter commands to push (one per line)")

    class Meta:
        name = "Huawei Backup & Config Tool"
        description = "Safe tool for Huawei S6720/S6730 Management"

    def run(self, data, commit):
        # Check 1: Library Check
        if not NETMIKO_LOADED:
            self.log_failure("CRITICAL: 'netmiko' library not found in NetBox container. Run 'pip install netmiko' in the worker.")
            return

        target_device = data['device']
        
        # Check 2: IP Check
        if not target_device.primary_ip:
            self.log_failure(f"Device {target_device.name} has no Primary IP in NetBox.")
            return
        
        ip_addr = str(target_device.primary_ip.address.ip)

        conn_params = {
            'device_type': 'huawei',
            'host': ip_addr,
            'username': data['username'],
            'password': data['password'],
            'conn_timeout': 20,
        }

        try:
            self.log_info(f"Connecting to {target_device.name} ({ip_addr})...")
            with ConnectHandler(**conn_params) as net_connect:
                self.log_success("Connected.")

                # PHASE 1: BACKUP
                if data['do_backup']:
                    self.log_info("Running Backup...")
                    backup_output = net_connect.send_command("display current-configuration")
                    # You can see the backup in the script log
                    self.log_debug(f"BACKUP CONTENT:\n{backup_output}")
                    self.log_success("Backup captured successfully.")

                # PHASE 2: CONFIGURATION
                if data['commands']:
                    cmd_list = data['commands'].strip().splitlines()
                    self.log_info(f"Pushing {len(cmd_list)} commands...")
                    config_output = net_connect.send_config_set(cmd_list)
                    self.log_info(f"DEVICE OUTPUT:\n{config_output}")
                    self.log_success("Configuration push complete.")

        except Exception as e:
            self.log_failure(f"Operation Failed: {str(e)}")

        return "Process Finished"
