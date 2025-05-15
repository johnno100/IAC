# Dell PowerEdge T440 Integration Guide

This guide provides step-by-step instructions for integrating a Dell PowerEdge T440 server into your existing infrastructure. The implementation combines Proxmox virtualization, Docker containers, and a comprehensive set of tools for infrastructure management.

## Table of Contents

1. [Implementation Overview](#implementation-overview)
2. [Prerequisites](#prerequisites)
3. [Phase 1: Foundation Setup](#phase-1-foundation-setup)
4. [Phase 2: Infrastructure Services](#phase-2-infrastructure-services)
5. [Phase 3: Core Services](#phase-3-core-services)
6. [Phase 4: AI Services](#phase-4-ai-services)
7. [Phase 5: Monitoring & Management](#phase-5-monitoring--management)
8. [Phase 6: Documentation & Governance](#phase-6-documentation--governance)
9. [Maintenance & Operations](#maintenance--operations)

## Implementation Overview

This implementation integrates your T440 with your existing Proxmox infrastructure to create a highly available cluster, with services distributed across both nodes for optimal resource utilization and redundancy.

### Architectural Components

- **Proxmox Cluster**: Two-node cluster with your existing node and the new T440
- **Docker Hosts**: VM-based Docker hosts with Portainer for management
- **Core Services**: Traefik, Authentik, and other infrastructure services
- **AI Platform**: OpenWebUI and related AI services
- **Monitoring Stack**: Prometheus, Grafana, and other monitoring tools
- **Documentation**: MkDocs-based technical documentation

## Prerequisites

Before starting the implementation, ensure you have:

- Your existing Proxmox node is operational
- The Dell PowerEdge T440 is racked and powered
- Network connectivity between both servers
- Administrative access to both systems
- Domain names configured for services (if applicable)
- Basic familiarity with Ansible, Proxmox, and Docker

## Phase 1: Foundation Setup

### Step 1: Clone the Repository

```bash
# Clone the repository to your control machine
git clone https://github.com/johnno100/IAC.git
cd IAC

# Create the vault password file
echo "your-secure-password" > .vault_pass
chmod 600 .vault_pass
```

### Step 2: Update Inventory

Edit the inventory file to match your environment:

```bash
# Edit the inventory file
nano ansible/inventory/production/hosts.yml

# Update the IP addresses, hostnames, and other details
```

### Step 3: Initialize Proxmox on T440

If Proxmox is not already installed on the T440:

```bash
# Download Proxmox VE ISO
wget https://enterprise.proxmox.com/iso/proxmox-ve_7.4-1.iso

# Create a bootable USB drive
dd if=proxmox-ve_7.4-1.iso of=/dev/sdX bs=1M status=progress

# Boot the T440 from the USB drive and follow the installation prompts
# - Set the hostname to 'pve2' or your preferred name
# - Configure networking according to your environment
# - Complete the installation and reboot
```

### Step 4: Run the Initial Setup Playbook

```bash
# Run the initial setup playbook
ansible-playbook -i ansible/inventory/production ansible/playbooks/initial-setup.yml
```

This playbook will:

- Configure networking on both Proxmox nodes
- Create the Proxmox cluster
- Join the T440 to the cluster
- Configure basic security settings

### Step 5: Verify Cluster Configuration

```bash
# SSH to either Proxmox node
ssh root@192.168.1.101

# Check cluster status
pvecm status

# Verify network connectivity between nodes
ping 10.10.10.2
```

## Phase 2: Infrastructure Services

### Step 1: Deploy Docker Host VMs

```bash
# Run the VM deployment playbook
ansible-playbook -i ansible/inventory/production ansible/playbooks/deploy-vms.yml
```

This playbook will:

- Create a Docker host VM on the T440
- Configure networking and storage
- Install Docker and related tools

### Step 2: Deploy HashiCorp Vault

```bash
# Deploy HashiCorp Vault
ansible-playbook -i ansible/inventory/production ansible/playbooks/deploy-vault.yml
```

This deploys HashiCorp Vault for secrets management.

### Step 3: Deploy Netbox for Infrastructure Documentation

```bash
# Deploy Netbox
ansible-playbook -i ansible/inventory/production ansible/playbooks/deploy-netbox.yml
```

This deploys Netbox for documenting your infrastructure.

## Phase 3: Core Services

### Step 1: Deploy Traefik

```bash
# Deploy Traefik
ansible-playbook -i ansible/inventory/production ansible/playbooks/deploy-traefik.yml
```

This deploys Traefik as your edge router and load balancer.

### Step 2: Deploy Authentik

```bash
# Deploy Authentik
ansible-playbook -i ansible/inventory/production ansible/playbooks/deploy-authentik.yml
```

This deploys Authentik as your identity provider.

### Step 3: Deploy Portainer

```bash
# Deploy Portainer
ansible-playbook -i ansible/inventory/production ansible/playbooks/deploy-portainer.yml
```

This deploys Portainer for container management.

## Phase 4: AI Services

### Step 1: Deploy OpenWebUI

```bash
# Deploy OpenWebUI
ansible-playbook -i ansible/inventory/production ansible/playbooks/deploy-openwebui.yml
```

This deploys OpenWebUI with PostgreSQL for AI interface.

## Phase 5: Monitoring & Management

### Step 1: Deploy Monitoring Stack

```bash
# Deploy monitoring stack
ansible-playbook -i ansible/inventory/production ansible/playbooks/deploy-monitoring.yml
```

This deploys Prometheus, Grafana, and other monitoring tools.

### Step 2: Deploy Uptime Kuma

```bash
# Deploy Uptime Kuma
ansible-playbook -i ansible/inventory/production ansible/playbooks/deploy-uptime-kuma.yml
```

This deploys Uptime Kuma for basic uptime monitoring.

### Step 3: Configure Backup System

```bash
# Configure backup system
ansible-playbook -i ansible/inventory/production ansible/playbooks/configure-backups.yml
```

This configures automated backups for all components.

## Phase 6: Documentation & Governance

### Step 1: Build Documentation

```bash
# Set up documentation
ansible-playbook ansible/playbooks/setup-documentation.yml

# Build documentation
cd docs
mkdocs serve
```

### Step 2: Initial Data Entry in Netbox

1. Access Netbox at <http://netbox-ip:8000>
2. Log in with the admin credentials
3. Add both Proxmox nodes as devices
4. Document the network topology
5. Add all VMs and services

### Step 3: Configure Monitoring Dashboard

1. Access Grafana at <http://grafana-ip:3000>
2. Log in with admin credentials
3. Configure dashboards for
   - Proxmox nodes
   - Docker hosts
   - Services

## Maintenance & Operations

### Regular Maintenance Tasks

- **Weekly**: Review monitoring dashboards
- **Monthly**: Test backup restoration
- **Quarterly**: Update documentation
- **Bi-annual**: Review security configurations

### Common Operations

- **Adding New VMs**:

  ```bash
  # Use the VM creation playbook
  ansible-playbook -i ansible/inventory/production ansible/playbooks/create-vm.yml -e "vm_name=newvm vm_id=123"
  ```

- **Deploying New Containers**:
  Use Portainer or the container deployment playbook:

  ```bash
  ansible-playbook -i ansible/inventory/production ansible/playbooks/deploy-container.yml -e "container_name=myapp container_image=myapp:latest"
  ```

- **Restoring from Backup**:

  ```bash
  # For VM restoration
  ansible-playbook -i ansible/inventory/production ansible/playbooks/restore-vm.yml -e "vm_id=123 backup_file=/path/to/backup"
  
  # For container volume restoration
  ansible-playbook -i ansible/inventory/production ansible/playbooks/restore-volume.yml -e "volume_name=myvolume backup_file=/path/to/backup"
  ```

### Troubleshooting

- **Cluster Issues**: Check `/var/log/pve-cluster/` on both nodes
- **VM Issues**: Check VM logs in Proxmox web interface
- **Container Issues**: Check logs via Portainer or `docker logs <container>`
- **Network Issues**: Check Proxmox firewall and network configurations

## Conclusion

By following this guide, you'll have a fully integrated Dell PowerEdge T440 server as part of your infrastructure, with a comprehensive set of services and tools for management, monitoring, and documentation.
