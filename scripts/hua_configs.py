from extras.scripts import Script, StringVar, TextVar, PasswordVar
from netmiko import ConnectHandler

class HuaweiConfigScript(Script):
    # These variables create the input form in the NetBox Web UI
    target_ip = StringVar(
        label="Target IP Address",
        description="IP address of the Huawei switch"
    )
    username = StringVar(
        label="SSH Username",
        default="venkatasatya.teja"
    )
    password = PasswordVar(
        label="SSH Password",
        default="Login@999"
    )
    commands = TextVar(
        label="Commands",
        description="Enter commands (one per line). Do not include 'system-view'."
    )

    class Meta:
        name = "Huawei Configuration Tool"
        description = "Push configurations to Huawei S6720/S6730 switches via Netmiko"

    def run(self, data, commit):
        # Extract data from the NetBox form
        target_ip = data['target_ip']
        username = data['username']
        password = data['password']
        # Convert the multi-line text input into a list of commands
        commands_list = data['commands'].strip().splitlines()

        if not commands_list:
            self.log_failure("No commands provided.")
            return

        huawei_device = {
            'device_type': 'huawei',
            'host': target_ip,
            'username': username,
            'password': password,
            'port': 22,
        }

        self.log_info(f"Connecting to {target_ip}...")

        try:
            with ConnectHandler(**huawei_device) as net_connect:
                self.log_success(f"Connected to {target_ip}")
                
                # Send commands; Netmiko handles 'system-view'/config mode automatically
                output = net_connect.send_config_set(commands_list)
                
                self.log_info("DEVICE OUTPUT:")
                self.log_debug(output)
                
                self.log_success("Configuration completed successfully.")
                
        except Exception as e:
            self.log_failure(f"Connection/Config Error: {str(e)}")

        return "Task Finished"
