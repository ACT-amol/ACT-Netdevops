from nornir import InitNornir

try:
    nr = InitNornir(config_file="config.yaml")
    print(f"✅ Success! Nornir connected to NetBox.")
    print(f"Found {len(nr.inventory.hosts)} devices:")
    for name, host in nr.inventory.hosts.items():
        print(f" - Device: {name} (IP: {host.hostname})")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
