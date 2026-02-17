from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config, netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.inventory import ConnectionOptions

def configure_network(task):
    platform_raw = task.host.platform
    platform_name = str(platform_raw).lower() if platform_raw else ""
    
    # 1. Logic for Huawei
    if "huawei" in platform_name:
        config_cmds = [
            "system-view",
            f"header shell information \"Welcome to {task.host.name}\"",
            "interface Vlanif1",
            "description Managed_by_Gemini_Nornir",
            "return"
        ]
        save_cmd = "save\ny" # Sends 'y' to confirm saving
    
    # 2. Logic for Juniper (GICEB-SW1)
    else:
        config_cmds = [
            f"set system host-name {task.host.name}",
        ]
        save_cmd = "commit"

    # Push Configuration with a higher delay factor
    task.run(
        task=netmiko_send_config, 
        config_commands=config_cmds,
        delay_factor=2
    )

    # Save Changes
    task.run(task=netmiko_send_command, command_string=save_cmd)

def main():
    nr = InitNornir(config_file="config.yaml")

    for hostname, host_obj in nr.inventory.hosts.items():
        host_obj.username = "venkatasatya.teja"
        host_obj.password = "Login@999"
        
        platform_str = str(host_obj.platform).lower() if host_obj.platform else ""
        
        # FIX: We use 'huawei' or 'juniper_junos'
        # If it still fails, we can use 'generic_termserver' to force a raw connection
        d_type = "huawei" if "huawei" in platform_str else "juniper_junos"
        
        host_obj.connection_options["netmiko"] = ConnectionOptions(
            extras={
                "device_type": d_type,
                "global_delay_factor": 2,
                "read_timeout": 60,
                "session_preparation": False  # This skips the 'Screen width' check
            }
        )

    result = nr.run(task=configure_network)
    print_result(result)

if __name__ == "__main__":
    main()
