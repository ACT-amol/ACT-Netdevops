import getpass
import sys
# Make sure to run: pip install netmiko
from netmiko import ConnectHandler

# --- OPTIONAL: HARDCODE CREDENTIALS ---
# If you don't want to type these every time, enter them inside the quotes below.
# WARNING: Be careful sharing this file if you save your password here.
DEFAULT_USERNAME = "venkatasatya.teja"  # Example: "admin"
DEFAULT_PASSWORD = "Login@999"  # Example: "Huawei@123"
# --------------------------------------

def configure_huawei():
    print("--- Huawei S6720/S6730 Configuration Tool ---")
    
    # 1. Get Connection Details
    try:
        target_ip = input("Target IP Address: ").strip()
        if not target_ip:
            print("Error: IP is required.")
            return

        # Check if username is hardcoded at top of file
        if DEFAULT_USERNAME:
            username = DEFAULT_USERNAME
            print(f"Using default username: {username}")
        else:
            username = input("SSH Username: ").strip()

        # Check if password is hardcoded at top of file
        if DEFAULT_PASSWORD:
            password = DEFAULT_PASSWORD
            print("Using default password.")
        else:
            password = getpass.getpass("SSH Password: ")

    except KeyboardInterrupt:
        print("\nExiting.")
        sys.exit()
    
    # 2. Get Commands
    print("\nEnter config commands one by one.")
    print("Type 'END' (case insensitive) on a new line to finish and run them.")
    print("-" * 40)
    
    commands = []
    while True:
        try:
            line = input("> ")
            if line.strip().upper() == 'END':
                break
            commands.append(line)
        except KeyboardInterrupt:
            print("\nCancelled.")
            sys.exit()

    if not commands:
        print("No commands entered. Exiting.")
        return

    # 3. Connect and Configure
    huawei_device = {
        'device_type': 'huawei',
        'host': target_ip,
        'username': username,
        'password': password,
        'port': 22,
        # 'global_delay_factor': 2, # Increase if network is slow
    }

    print(f"\nConnecting to {target_ip}...")
    
    try:
        with ConnectHandler(**huawei_device) as net_connect:
            print("✅ Connected successfully.")
            
            # Optional: Show current version
            # print(net_connect.send_command("display version"))

            print(f"🚀 Sending {len(commands)} commands...")
            
            # send_config_set handles 'system-view' automatically
            output = net_connect.send_config_set(commands)
            
            print("\n" + "="*40)
            print("DEVICE OUTPUT:")
            print("="*40)
            print(output)
            print("="*40)
            print("✅ Configuration Complete.")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    configure_huawei()
