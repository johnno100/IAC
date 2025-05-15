# Infrastructure as Code Repository Structure and Setup Guide

This guide walks you through setting up the IAC repository structure for your infrastructure integration project, including all the necessary files and directories for integrating your Dell PowerEdge T440 with your existing Proxmox infrastructure.

## Complete Repository Structure

```markdown
IAC/
├── ansible/
│   ├── inventory/
│   │   ├── production/
│   │   │   ├── hosts.yml                     # Production inventory
│   │   │   ├── group_vars/                   # Production group variables
│   │   │   │   ├── all.yml
│   │   │   │   ├── proxmox_cluster.yml
│   │   │   │   └── docker_hosts.yml
│   │   │   └── host_vars/                     # Host-specific variables
│   │   └── staging/
│   │       ├── hosts.yml                     # Staging inventory
│   │       └── group_vars/                   # Staging group variables
│   ├── playbooks/
│   │   ├── initial-setup.yml                 # Initial infrastructure setup
│   │   ├── deploy-vms.yml                    # VM deployment
│   │   ├── deploy-monitoring.yml             # Monitoring stack
│   │   ├── deploy-containers.yml             # Container deployment
│   │   ├── deploy-openwebui.yml              # OpenWebUI deployment
│   │   ├── deploy-traefik.yml                # Traefik deployment
│   │   ├── deploy-authentik.yml              # Authentik deployment
│   │   ├── configure-backups.yml             # Backup configuration
│   │   └── setup-documentation.yml           # Documentation setup
│   ├── roles/
│   │   ├── proxmox/                          # Proxmox configuration role
│   │   │   ├── tasks/
│   │   │   ├── templates/
│   │   │   ├── defaults/
│   │   │   └── handlers/
│   │   ├── docker/                           # Docker setup role
│   │   ├── traefik/                          # Traefik configuration role
│   │   ├── authentik/                        # Authentik setup role
│   │   ├── openwebui/                        # OpenWebUI setup role
│   │   ├── monitoring/                       # Monitoring setup role
│   │   ├── vault/                            # HashiCorp Vault role
│   │   ├── netbox/                           # Netbox role
│   │   └── backup/                           # Backup configuration role
│   ├── vars/
│   │   ├── main.yml                          # Main variables
│   │   └── vault.yml                         # Encrypted sensitive variables
│   └── ansible.cfg                           # Ansible configuration
├── docs/
│   ├── docs/                                 # Documentation markdown files
│   │   ├── index.md                          # Home page
│   │   ├── architecture/                     # Architecture documentation
│   │   ├── infrastructure/                   # Infrastructure documentation
│   │   ├── services/                         # Services documentation
│   │   ├── operations/                       # Operational procedures
│   │   └── howtos/                           # How-to guides
│   ├── mkdocs.yml                            # MkDocs configuration
│   └── README.md                             # Documentation README
├── diagrams/                                 # Infrastructure diagrams
│   ├── network-topology.drawio               # Network topology diagram
│   └── infrastructure-overview.drawio        # Infrastructure overview diagram
├── scripts/                                  # Utility scripts
│   ├── setup.sh                              # Initial setup script
│   ├── backup-check.sh                       # Backup verification script
│   └── update-ansible.sh                     # Ansible update script
├── semaphore/                                # Semaphore configuration
│   ├── inventory.json                        # Semaphore inventory
│   ├── environment.json                      # Semaphore environment
│   └── project.json                          # Semaphore project
├── templates/                                # Configuration templates
│   ├── interfaces.j2                         # Network interfaces template
│   ├── hosts.j2                              # Hosts file template
│   ├── traefik.yml.j2                        # Traefik configuration template
│   └── docker-compose/                       # Docker Compose templates
│       ├── traefik.yml.j2                    # Traefik Docker Compose
│       ├── authentik.yml.j2                  # Authentik Docker Compose
│       ├── openwebui.yml.j2                  # OpenWebUI Docker Compose
│       └── monitoring.yml.j2                 # Monitoring Docker Compose
├── .gitignore                                # Git ignore file
├── .pre-commit-config.yaml                   # Pre-commit configuration
├── README.md                                 # Repository README
└── requirements.txt                          # Python requirements
```

## Setting Up the Repository

### 1. Create the Repository in GitHub

1. Go to GitHub and log in with your johnno100 account
2. Click the "+" icon in the top-right corner and select "New repository"
3. Set the repository name to "IAC"
4. Add a description: "Infrastructure as Code for Multiskilled AI environment"
5. Keep it as a public repository
6. Initialize with a README.md
7. Click "Create repository"

### 2. Clone the Repository Locally

```bash
# Clone the repository to your local machine
git clone https://github.com/johnno100/IAC.git
cd IAC
```

### 3. Create the Directory Structure

```bash
# Create main directories
mkdir -p ansible/{inventory/{production,staging}/{group_vars,host_vars},playbooks,roles,vars}
mkdir -p docs/docs/{architecture,infrastructure,services,operations,howtos}
mkdir -p diagrams scripts semaphore templates/docker-compose
```

### 4. Copy Base Files

Use the files provided in the artifacts to populate your repository:

1. Copy `root-readme.md` to `README.md`
2. Copy all inventory files to `ansible/inventory/`
3. Copy playbooks to `ansible/playbooks/`
4. Copy implementation guide to `docs/docs/index.md`

### 5. Set Up Ansible Configuration

Create `ansible/ansible.cfg`:

```ini
[defaults]
inventory = ./inventory/production
roles_path = ./roles
host_key_checking = False
retry_files_enabled = False
vault_password_file = ../.vault_pass

[privilege_escalation]
become = True
become_method = sudo
become_user = root
become_ask_pass = False

[ssh_connection]
pipelining = True
control_path = /tmp/ansible-ssh-%%h-%%p-%%r
```

### 6. Create a Vault Password File

```bash
# Generate a random password
openssl rand -base64 32 > .vault_pass
chmod 600 .vault_pass
```

### 7. Create Encrypted Vault File

```bash
# Create vault file with sensitive variables
cat > ansible/vars/vault.yml << 'EOF'
# Sensitive variables for infrastructure deployment
vault_grafana_admin_password: adminpassword
vault_authentik_admin_password: authentikpassword
vault_authentik_postgresql_password: dbpassword
vault_authentik_secret_key: secretkey
vault_authentik_admin_token: admintoken
vault_openwebui_db_password: openwebuipassword
EOF

# Encrypt the vault file
ansible-vault encrypt ansible/vars/vault.yml
```

### 8. Create Pre-commit Configuration

```bash
# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
- repo: https://github.com/ansible/ansible-lint
  rev: v6.17.0
  hooks:
    - id: ansible-lint
- repo: https://github.com/adrienverge/yamllint
  rev: v1.32.0
  hooks:
    - id: yamllint
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v4.4.0
  hooks:
    - id: trailing-whitespace
    - id: end-of-file-fixer
    - id: check-yaml
    - id: check-added-large-files
EOF
```

### 9. Set Up Semaphore Configuration (Optional)

If you're using Semaphore for Ansible management, create a basic Semaphore configuration:

```bash
# Create inventory.json
cat > semaphore/inventory.json << 'EOF'
{
  "name": "Production",
  "inventory": "ansible/inventory/production"
}
EOF

# Create project.json
cat > semaphore/project.json << 'EOF'
{
  "name": "IAC Project",
  "playbook_directory": "ansible/playbooks",
  "inventory_directory": "ansible/inventory"
}
EOF
```

### 10. Add Documentation Structure

MkDocs is used for documentation. Set up the initial structure:

```bash
# Create mkdocs.yml
cat > docs/mkdocs.yml << 'EOF'
site_name: AI Infrastructure Documentation
site_description: Technical documentation for our AI infrastructure
site_author: Your Organization

theme:
  name: material
  palette:
    primary: indigo
    accent: indigo
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - search.highlight
    - search.share

plugins:
  - search
  - diagrams

markdown_extensions:
  - admonition
  - attr_list
  - codehilite
  - footnotes
  - pymdownx.superfences
  - pymdownx.tabbed
  - pymdownx.tasklist

nav:
  - Home: index.md
  - Architecture:
      - Overview: architecture/overview.md
      - Network Topology: architecture/network-topology.md
  - Infrastructure:
      - Proxmox Cluster: infrastructure/proxmox-cluster.md
      - Docker Hosts: infrastructure/docker-hosts.md
  - Services:
      - Traefik: services/traefik.md
      - Authentik: services/authentik.md
      - OpenWebUI: services/openwebui.md
  - Operations:
      - Backup & Recovery: operations/backup-recovery.md
      - Monitoring: operations/monitoring.md
  - How-to Guides:
      - Adding VMs: howtos/adding-vms.md
      - Deploying Containers: howtos/deploying-containers.md
EOF
```

### 11. Create Utility Scripts

```bash
# Create setup.sh
cat > scripts/setup.sh << 'EOF'
#!/bin/bash
# Initial setup script for the IAC repository

# Install dependencies
pip install -r requirements.txt

# Set up pre-commit
pre-commit install

# Create vault password file if it doesn't exist
if [ ! -f .vault_pass ]; then
  echo "Creating vault password file..."
  openssl rand -base64 32 > .vault_pass
  chmod 600 .vault_pass
fi

echo "Setup complete!"
EOF
chmod +x scripts/setup.sh

# Create requirements.txt
cat > requirements.txt << 'EOF'
ansible>=8.0.0
docker>=6.1.3
proxmoxer>=2.0.1
requests>=2.31.0
pyyaml>=6.0.1
jinja2>=3.1.2
netaddr>=0.8.0
pre-commit>=3.3.3
mkdocs>=1.5.3
mkdocs-material>=9.4.5
pymdown-extensions>=10.3.1
EOF
```

### 12. Create Basic .gitignore

```bash
# Create .gitignore
cat > .gitignore << 'EOF'
# Python artifacts
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Ansible artifacts
*.retry

# Virtual environments
venv/
ENV/
env/

# Sensitive files
.vault_pass
*.key
*.pem

# MkDocs site
docs/site/

# Editor files
.vscode/
.idea/
*.swp
*.swo

# OS specific files
.DS_Store
Thumbs.db

# Diagram backups
diagrams/*.drawio.bkp
diagrams/*.drawio.dtmp
EOF
```

### 13. Initial Commit and Push

```bash
# Add all files to git
git add .

# Commit the changes
git commit -m "Initial repository setup for IAC project"

# Push to GitHub
git push origin main
```

## Next Steps

After setting up the repository structure, continue with:

1. **Complete the playbooks**: Develop and test the Ansible playbooks
2. **Set up Semaphore**: Configure Semaphore for easier Ansible management
3. **Document the infrastructure**: Fill out the documentation
4. **Implement the infrastructure**: Follow the implementation guide

## Using with Semaphore

If you're using Semaphore for Ansible execution:

1. Install Semaphore on your management server
2. Create a new project pointing to your GitHub repository
3. Configure the inventory, environment, and credentials
4. Set up jobs for the various playbooks

This provides a web interface for executing your Ansible playbooks and managing your infrastructure.
