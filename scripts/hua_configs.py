from extras.scripts import Script, StringVar, TextVar, PasswordVar
from netmiko import ConnectHandler

class HuaweiConfigScript(Script):
    # This replaces the input() calls with Web UI fields
    target_ip = StringVar(label="Target IP Address")
    username = StringVar(label="SSH Username", default="venkatasatya.teja")
    password = PasswordVar(label="SSH Password", default="Login@999")
    commands = TextVar(label="Configuration Commands", description="One command per line")

    class Meta:
        name = "Huawei Configuration Tool"
        description = "Push configs to Huawei S6720/S6730"

    def run(self, data, commit):
        # Setup device details from the form
        huawei_device = {
            'device_type': 'huawei',
            'host': data['target_ip'],
            'username': data['username'],
            'password': data['password'],
            'port': 22,
        }

        # Convert text box input to a list of commands
        commands_list = data['commands'].strip().splitlines()
        
        self.log_info(f"Connecting to {data['target_ip']}...")
        
        try:
            with ConnectHandler(**huawei_device) as net_connect:
                self.log_success("✅ Connected successfully.")
                
                # Send the commands
                output = net_connect.send_config_set(commands_list)
                
                self.log_info("DEVICE OUTPUT:")
                self.log_debug(output)
                self.log_success("✅ Configuration Complete.")
                
        except Exception as e:
            self.log_failure(f"❌ Error: {str(e)}")

        return "Done"
