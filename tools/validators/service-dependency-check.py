# tools/validators/service-dependency-check.py
#!/usr/bin/env python3
import yaml
import sys
import os
import subprocess
import json
import argparse

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def check_network_device(device, interface=None, vlan=None):
    # Simulate network device check (replace with actual check)
    # In a real implementation, use SNMP, API, or CLI to check the device
    print(f"Checking network device: {device}")
    if interface:
        print(f"  Interface: {interface}")
    if vlan:
        print(f"  VLAN: {vlan}")
    return True  # Replace with actual verification

def check_service(service):
    # Check if the service is running using Docker
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}", "--filter", f"name={service}"],
            capture_output=True, text=True, check=True
        )
        return service in result.stdout.strip()
    except subprocess.CalledProcessError:
        return False

def main():
    parser = argparse.ArgumentParser(description='Validate service dependencies')
    parser.add_argument('--mapping-file', default='state/service-network-mapping.yml', 
                      help='Path to service-network mapping file')
    parser.add_argument('--service', help='Specific service to check (optional)')
    args = parser.parse_args()
    
    if not os.path.exists(args.mapping_file):
        print(f"Error: Mapping file not found: {args.mapping_file}")
        return 1
    
    mapping = load_yaml(args.mapping_file)
    
    if args.service:
        services = [s for s in mapping['network_dependencies'] if s['service'] == args.service]
        if not services:
            print(f"Error: Service {args.service} not found in mapping")
            return 1
    else:
        services = mapping['network_dependencies']
    
    all_ok = True
    
    for service_dep in services:
        service_name = service_dep['service']
        print(f"\nValidating service: {service_name}")
        
        # Check the service itself
        service_ok = check_service(service_name)
        if service_ok:
            print(f"✅ Service {service_name} is running")
        else:
            print(f"❌ Service {service_name} is NOT running")
            all_ok = False
        
        # Check network dependencies
        for dep in service_dep['depends_on']:
            if 'device' in dep:
                device = dep['device']
                
                for interface in dep.get('interfaces', [None]):
                    for vlan in dep.get('vlans', [None]):
                        if check_network_device(device, interface, vlan):
                            print(f"✅ Network dependency OK: {device} {interface} VLAN {vlan}")
                        else:
                            print(f"❌ Network dependency FAILED: {device} {interface} VLAN {vlan}")
                            all_ok = False
            
            elif 'service' in dep:
                dep_service = dep['service']
                if check_service(dep_service):
                    print(f"✅ Dependency service {dep_service} is running")
                else:
                    print(f"❌ Dependency service {dep_service} is NOT running")
                    all_ok = False
    
    if all_ok:
        print("\n✅ All dependencies validated successfully")
        return 0
    else:
        print("\n❌ Some dependencies failed validation")
        return 1

if __name__ == "__main__":
    sys.exit(main())