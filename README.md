# Infrastructure as Code for Multiskilled AI Environment

This repository contains the complete Infrastructure as Code (IaC) implementation for setting up a Proxmox-based infrastructure with Docker containers, specialized AI services, and comprehensive monitoring. It's designed to integrate a Dell PowerEdge T440 server with an existing Proxmox setup, creating a robust platform for AI workloads.

## Repository Structure

```markdown
├── ansible/                    # Ansible configuration and playbooks
│   ├── inventory/              # Server inventory definitions
│   │   ├── production/         # Production environment
│   │   └── staging/            # Staging environment
│   ├── playbooks/              # Playbook definitions
│   ├── roles/                  # Reusable role definitions
│   └── vars/                   # Variable definitions
├── docs/                       # Project documentation (MkDocs)
├── semaphore/                  # Semaphore configuration
├── scripts/                    # Utility scripts
└── templates/                  # Configuration templates
```

## Getting Started

### Prerequisites

Before beginning implementation, ensure you have:

1. An existing Proxmox node with a Docker host VM
2. A Dell PowerEdge T440 server ready for deployment
3. Network connectivity between both servers
4. Administrative access to both systems
5. Git and Ansible installed on your control machine

### Quick Start

1. Clone this repository:

   ```bash

   git clone https://github.com/johnno100/IAC.git
   cd IAC
   ```

2. Update the inventory with your server information:

   ```bash
   nano ansible/inventory/production/hosts.yml
   ```

3. Run the initial setup playbook:

   ```bash
   ansible-playbook -i ansible/inventory/production ansible/playbooks/initial-setup.yml
   ```

## Implementation Phases

The implementation is organized into the following phases:

1. **Foundation Setup**: Prepare both Proxmox nodes and create cluster
2. **Storage Configuration**: Set up shared or distributed storage
3. **Network Configuration**: Configure VLANs and network isolation
4. **Monitoring Implementation**: Deploy monitoring tools
5. **Core Services Deployment**: Deploy Traefik, Authentik, etc.
6. **AI Platform Deployment**: Deploy OpenWebUI and related services

Each phase has dedicated playbooks and documentation.

## Documentation

Comprehensive documentation is available in the `docs/` directory, covering:

- Detailed architecture diagrams
- Step-by-step implementation guides
- Troubleshooting procedures
- Backup and recovery processes

Build the documentation site:

```bash
cd docs
mkdocs serve
```

## Toolset

This infrastructure leverages the following tools:

- **Proxmox VE**: Virtualization platform
- **Docker/Portainer**: Container management
- **Ansible**: Configuration management
- **Semaphore**: Ansible GUI and job scheduling
- **HashiCorp Vault**: Secrets management
- **Traefik**: Edge router and load balancer
- **Authentik**: Identity provider
- **Uptime Kuma**: Basic monitoring
- **Prometheus/Grafana**: Advanced monitoring
- **Netbox**: Infrastructure documentation
- **MkDocs**: Technical documentation
- **Draw.io**: Infrastructure diagramming

## License

This project is licensed under the MIT License - see the LICENSE file for details.
