# tools/state-diff/generate-migration-plan.py
#!/usr/bin/env python3
import yaml
import os
import sys
import argparse
from datetime import datetime

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_migration_tasks(current, target, device_name):
    tasks = []
    
    # Generate VLAN changes
    current_vlans = {v['id']: v for v in current.get('vlans', [])}
    target_vlans = {v['id']: v for v in target.get('vlans', [])}
    
    for vlan_id in set(target_vlans.keys()) - set(current_vlans.keys()):
        vlan = target_vlans[vlan_id]
        tasks.append({
            'name': f"Create VLAN {vlan_id} ({vlan['name']})",
            'ansible.netcommon.cli_config': {
                'config': f"vlan {vlan_id}\n name {vlan['name']}"
            }
        })
    
    # Generate interface changes
    current_ifs = {i['name']: i for i in current.get('interfaces', [])}
    target_ifs = {i['name']: i for i in target.get('interfaces', [])}
    
    for if_name in set(target_ifs.keys()) - set(current_ifs.keys()):
        interface = target_ifs[if_name]
        config_lines = [f"interface {if_name}"]
        
        if 'description' in interface:
            config_lines.append(f" description \"{interface['description']}\"")
        
        if interface.get('vlan') == 'trunk':
            vlans_str = ','.join(str(v) for v in interface.get('vlans', []))
            config_lines.append(f" switchport mode trunk")
            config_lines.append(f" switchport trunk allowed vlan {vlans_str}")
        elif 'vlan' in interface:
            config_lines.append(f" switchport mode access")
            config_lines.append(f" switchport access vlan {interface['vlan']}")
        
        tasks.append({
            'name': f"Configure interface {if_name}",
            'ansible.netcommon.cli_config': {
                'config': '\n'.join(config_lines)
            }
        })
    
    # Package into a playbook
    playbook = [{
        'name': f"Network Migration for {device_name}",
        'hosts': device_name,
        'gather_facts': False,
        'tasks': tasks
    }]
    
    return playbook

def main():
    parser = argparse.ArgumentParser(description='Generate migration plan from current to target state')
    parser.add_argument('--current-dir', default='state/current/network', help='Directory with current state files')
    parser.add_argument('--target-dir', default='state/target/network', help='Directory with target state files')
    parser.add_argument('--output-dir', default='state/migrations', help='Directory for migration plans')
    parser.add_argument('--device', help='Specific device to process (optional)')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y%m%d")
    
    if args.device:
        devices = [args.device]
    else:
        # Find all devices in current and target directories
        current_files = [os.path.splitext(f)[0] for f in os.listdir(args.current_dir) if f.endswith('.yml')]
        target_files = [os.path.splitext(f)[0] for f in os.listdir(args.target_dir) if f.endswith('.yml')]
        devices = sorted(set(current_files).intersection(set(target_files)))
    
    for device in devices:
        current_file = os.path.join(args.current_dir, f"{device}.yml")
        target_file = os.path.join(args.target_dir, f"{device}.yml")
        
        if not os.path.exists(current_file) or not os.path.exists(target_file):
            print(f"Skipping {device}: missing current or target file")
            continue
        
        current = load_yaml(current_file)
        target = load_yaml(target_file)
        
        migration = generate_migration_tasks(current, target, device)
        
        output_file = os.path.join(args.output_dir, f"{date_str}-{device}-migration.yml")
        with open(output_file, 'w') as f:
            yaml.dump(migration, f, default_flow_style=False)
        
        print(f"Generated migration plan for {device}: {output_file}")

if __name__ == "__main__":
    sys.exit(main())