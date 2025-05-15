# Semaphore Setup and Configuration Guide

This guide walks you through setting up Semaphore, a modern web UI for Ansible, to manage your infrastructure deployments through a user-friendly interface.

## What is Semaphore?

Semaphore is an open-source alternative to Ansible Tower/AWX that provides:

- Web-based interface for executing Ansible playbooks
- Role-based access control
- Playbook scheduling
- Inventory management
- Credential management
- Task history and logging

## Installation

### Option 1: Docker Deployment (Recommended)

1. Create a directory for Semaphore:

```bash
mkdir -p /opt/semaphore/config
cd /opt/semaphore
```

2. Create a Docker Compose file:

```bash
cat > docker-compose.yml << 'EOF'
version: '3'

services:
  postgres:
    image: postgres:13
    container_name: semaphore-postgres
    environment:
      POSTGRES_USER: semaphore
      POSTGRES_PASSWORD: semaphore_password
      POSTGRES_DB: semaphore
    volumes:
      - semaphore-postgres:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - semaphore-network

  semaphore:
    image: semaphoreui/semaphore:latest
    container_name: semaphore
    ports:
      - "3000:3000"
    environment:
      SEMAPHORE_DB_USER: semaphore
      SEMAPHORE_DB_PASS: semaphore_password
      SEMAPHORE_DB_HOST: postgres
      SEMAPHORE_DB_PORT: 5432
      SEMAPHORE_DB_DIALECT: postgres
      SEMAPHORE_DB: semaphore
      SEMAPHORE_PLAYBOOK_PATH: /tmp/semaphore/
      SEMAPHORE_ADMIN_PASSWORD: changeme
      SEMAPHORE_ADMIN_NAME: admin
      SEMAPHORE_ADMIN_EMAIL: admin@localhost
      SEMAPHORE_ADMIN: admin
      SEMAPHORE_WEB_ROOT: http://localhost:3000
    volumes:
      - ./config:/etc/semaphore
      - ~/.ssh:/root/.ssh:ro
      - ./inventory:/tmp/semaphore/inventory
      - ./playbooks:/tmp/semaphore/playbooks
      - ./keys:/tmp/semaphore/keys
    depends_on:
      - postgres
    restart: unless-stopped
    networks:
      - semaphore-network
      - web

volumes:
  semaphore-postgres:

networks:
  semaphore-network:
  web:
    external: true
EOF
```

3. Create necessary directories for Semaphore:
```bash
mkdir -p inventory playbooks keys
chmod 700 keys
```

4. Deploy Semaphore:
```bash
docker-compose up -d
```

### Option 2: Direct Installation

For bare-metal installation:

```bash
# Download the latest release
curl -L https://github.com/ansible-semaphore/semaphore/releases/latest/download/semaphore_linux_amd64 -o /usr/local/bin/semaphore
chmod +x /usr/local/bin/semaphore

# Setup semaphore
mkdir -p /etc/semaphore
semaphore setup

# Run as a service
cat > /etc/systemd/system/semaphore.service << 'EOF'
[Unit]
Description=Ansible Semaphore
Documentation=https://github.com/ansible-semaphore/semaphore
Wants=network-online.target
After=network-online.target

[Service]
ExecStart=/usr/local/bin/semaphore -config /etc/semaphore/config.json
Restart=on-failure
RestartSec=10s
SyslogIdentifier=semaphore

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
systemctl enable semaphore
systemctl start semaphore
```

## Integrating with Your GitHub Repository

### 1. Create an SSH Key for Repository Access

```bash
# Generate SSH key for GitHub access
ssh-keygen -t ed25519 -f ./keys/github-key -C "semaphore@example.com"
chmod 600 ./keys/github-key

# Display the public key to add to GitHub
cat ./keys/github-key.pub
```

Add this key as a deploy key to your GitHub repository:
1. Go to your GitHub repository (https://github.com/johnno100/IAC)
2. Navigate to Settings > Deploy keys
3. Click "Add deploy key"
4. Paste the public key content
5. Enable "Allow write access" if needed
6. Click "Add key"

### 2. Initial Semaphore Configuration

Access Semaphore at http://your-server:3000 and log in with the default credentials:
- Username: admin
- Password: changeme (or the one you set in the environment variables)

### 3. Configure Semaphore Project

1. **Add Key**:
   - Go to Key Store
   - Click "New Key"
   - Name: "GitHub Deploy Key"
   - Type: SSH
   - Paste the private key content from `./keys/github-key`
   - Click "Create"

2. **Add Environment**:
   - Go to Environment
   - Click "New Environment"
   - Name: "Production"
   - Click "Create"
   - Add environment variables:
     - `ANSIBLE_HOST_KEY_CHECKING`: false
     - `ANSIBLE_FORCE_COLOR`: true

3. **Add Inventory**:
   - Go to Inventory
   - Click "New Inventory"
   - Name: "Production"
   - Type: "File"
   - Set the inventory path to match your repository structure: 
     ```
     ansible/inventory/production
     ```
   - Click "Create"

4. **Add Repository**:
   - Go to Repositories
   - Click "New Repository"
   - Name: "IAC Repository"
   - Git URL: `git@github.com:johnno100/IAC.git`
   - Branch: main
   - SSH Key: Select "GitHub Deploy Key"
   - Click "Create"

5. **Add Project**:
   - Go to Projects
   - Click "Add Project"
   - Name: "Infrastructure Deployment"
   - Inventory: "Production"
   - Repository: "IAC Repository"
   - Environment: "Production"
   - Playbook Path: "ansible/playbooks/initial-setup.yml" (as a starting point)
   - Click "Create"

### 4. Run Your First Task

1. Go to the "Infrastructure Deployment" project
2. Click "Tasks" in the top menu
3. Click "Run" button
4. Select the playbook to run (e.g., "ansible/playbooks/initial-setup.yml")
5. Click "Run Task"

## Setting Up User Access

For teams, you'll want to set up additional users with appropriate permissions:

1. Go to Users
2. Click "Add User"
3. Provide the user details
4. Assign appropriate roles:
   - Admin: Full access to Semaphore
   - Regular: Can run tasks but can't manage users
   - Read Only: Can only view task statuses

## Setting Up Scheduled Tasks

For routine operations like backups:

1. Go to your project
2. Click "Templates"
3. Click "New Template"
4. Configure the template:
   - Name: "Daily Backup"
   - Playbook: "ansible/playbooks/configure-backups.yml"
   - Environment: "Production"
   - Inventory: "Production"
5. Click "Create"
6. Go to the Templates tab
7. Click "Schedule" next to your template
8. Configure the CRON schedule (e.g., `0 2 * * *` for 2 AM daily)
9. Click "Create"

## Best Practices for Semaphore

1. **Organize with Templates**:
   Create templates for common operations to standardize execution

2. **Implement Access Control**:
   Restrict access based on roles and responsibilities

3. **Monitor Task History**:
   Regularly review the task history for failures

4. **Use Environment Variables**:
   Store configuration in environments rather than hardcoding

5. **Backup Semaphore Database**:
   Regularly backup the Postgres database that stores Semaphore configuration

## Troubleshooting

### Common Issues and Solutions

1. **Connection Issues to GitHub**:
   - Verify the deploy key has proper permissions
   - Check SSH key formatting
   - Ensure the repository URL is correct

2. **Playbook Execution Failures**:
   - Check the detailed logs in the task view
   - Verify environment variables
   - Ensure the inventory is accessible

3. **Database Connection Issues**:
   - Check Postgres container status
   - Verify database credentials

4. **Performance Problems**:
   - Increase resources for the Semaphore container
   - Monitor database growth and optimize if needed

## Semaphore Project Structure Example

For complex infrastructures, organize your projects in Semaphore as follows:

1. **Infrastructure Base**:
   - Initial setup playbooks
   - Network configuration
   - Proxmox cluster formation

2. **Core Services**:
   - Traefik deployment
   - Authentik setup
   - Monitoring implementation

3. **Application Services**:
   - OpenWebUI deployment
   - Additional AI services

4. **Maintenance Operations**:
   - Backup configuration
   - Update procedures
   - Security audits

This organization provides clear separation of concerns and targeted access control.