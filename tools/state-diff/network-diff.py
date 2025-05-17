# tools/state-diff/network-diff.py
#!/usr/bin/env python3
import yaml
import sys
import os
import difflib
import argparse
from colorama import Fore, Style, init

# Initialize colorama
init()

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def compare_devices(current, target):
    # Compare basic device attributes
    changes = []
    if current['device'] != target['device']:
        changes.append(f"Device properties will change: {current['device']} -> {target['device']}")
    
    # Compare VLANs
    current_vlans = {v['id']: v for v in current.get('vlans', [])}
    target_vlans = {v['id']: v for v in target.get('vlans', [])}
    
    for vlan_id in set(current_vlans.keys()) - set(target_vlans.keys()):
        changes.append(f"VLAN {vlan_id} ({current_vlans[vlan_id]['name']}) will be REMOVED")
    
    for vlan_id in set(target_vlans.keys()) - set(current_vlans.keys()):
        changes.append(f"VLAN {vlan_id} ({target_vlans[vlan_id]['name']}) will be ADDED")
    
    for vlan_id in set(current_vlans.keys()) & set(target_vlans.keys()):
        if current_vlans[vlan_id] != target_vlans[vlan_id]:
            changes.append(f"VLAN {vlan_id} will be MODIFIED: {current_vlans[vlan_id]} -> {target_vlans[vlan_id]}")
    
    # Compare interfaces (similar logic to VLANs)
    current_ifs = {i['name']: i for i in current.get('interfaces', [])}
    target_ifs = {i['name']: i for i in target.get('interfaces', [])}
    
    for if_name in set(current_ifs.keys()) - set(target_ifs.keys()):
        changes.append(f"Interface {if_name} will be REMOVED")
    
    for if_name in set(target_ifs.keys()) - set(current_ifs.keys()):
        changes.append(f"Interface {if_name} will be ADDED")
    
    for if_name in set(current_ifs.keys()) & set(target_ifs.keys()):
        if current_ifs[if_name] != target_ifs[if_name]:
            changes.append(f"Interface {if_name} will be MODIFIED: {current_ifs[if_name]} -> {target_ifs[if_name]}")
    
    return changes

def main():
    parser = argparse.ArgumentParser(description='Compare current and target network configuration')
    parser.add_argument('--current-dir', default='state/current/network', help='Directory with current state files')
    parser.add_argument('--target-dir', default='state/target/network', help='Directory with target state files')
    parser.add_argument('--device', help='Specific device to compare (optional)')
    args = parser.parse_args()
    
    if args.device:
        current_file = os.path.join(args.current_dir, f"{args.device}.yml")
        target_file = os.path.join(args.target_dir, f"{args.device}.yml")
        
        if not os.path.exists(current_file):
            print(f"Error: Current state file for {args.device} not found")
            return 1
        if not os.path.exists(target_file):
            print(f"Error: Target state file for {args.device} not found")
            return 1
        
        current = load_yaml(current_file)
        target = load_yaml(target_file)
        changes = compare_devices(current, target)
        
        print(f"{Fore.CYAN}Changes for {args.device}:{Style.RESET_ALL}")
        for change in changes:
            if "ADDED" in change:
                print(f"{Fore.GREEN}{change}{Style.RESET_ALL}")
            elif "REMOVED" in change:
                print(f"{Fore.RED}{change}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}{change}{Style.RESET_ALL}")
    else:
        # Compare all devices in the directories
        current_files = [f for f in os.listdir(args.current_dir) if f.endswith('.yml')]
        target_files = [f for f in os.listdir(args.target_dir) if f.endswith('.yml')]
        
        all_devices = set([os.path.splitext(f)[0] for f in current_files + target_files])
        
        for device in sorted(all_devices):
            current_file = os.path.join(args.current_dir, f"{device}.yml")
            target_file = os.path.join(args.target_dir, f"{device}.yml")
            
            if not os.path.exists(current_file):
                print(f"{Fore.GREEN}New device: {device}{Style.RESET_ALL}")
                continue
            if not os.path.exists(target_file):
                print(f"{Fore.RED}Removed device: {device}{Style.RESET_ALL}")
                continue
            
            current = load_yaml(current_file)
            target = load_yaml(target_file)
            changes = compare_devices(current, target)
            
            if changes:
                print(f"\n{Fore.CYAN}Changes for {device}:{Style.RESET_ALL}")
                for change in changes:
                    if "ADDED" in change:
                        print(f"{Fore.GREEN}  {change}{Style.RESET_ALL}")
                    elif "REMOVED" in change:
                        print(f"{Fore.RED}  {change}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}  {change}{Style.RESET_ALL}")

if __name__ == "__main__":
    sys.exit(main())