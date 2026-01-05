from nornir import InitNornir
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.files import write_file

def generate_configs(task):
    # 1. Take the Jinja template and inject NetBox data
    result = task.run(
        task=template_file,
        template="juniper_ex.j2",
        path="templates"
    )
    
    # 2. Save the result to the 'rendered' folder
    # This creates a file named like 'GICEB-SW1.conf'
    task.run(
        task=write_file,
        content=result.result,
        filename=f"rendered/{task.host.name}.conf"
    )

def main():
    # Initialize Nornir using our config.yaml (located in the root folder)
    nr = InitNornir(config_file="config.yaml")
    
    # Run the generate_configs function for every device found in NetBox
    nr.run(task=generate_configs)
    
    print("\n✅ Success! Check the 'rendered/' folder for your Juniper config files.\n")

if __name__ == "__main__":
    main()
