# Deployment Checklist

## Pre-Deployment Verification

- [ ] All hosts are reachable via SSH
- [ ] All network paths have been validated
- [ ] DNS resolution is working for all services
- [ ] Sufficient resources available on all hosts
- [ ] Pre-deployment validation playbook completed successfully
- [ ] State comparison has been reviewed and approved
- [ ] Migration plan has been reviewed and approved
- [ ] Backup of current configuration has been taken

## Deployment Sequence

1. [ ] Network infrastructure changes
   - [ ] VLAN creation
   - [ ] Interface configuration
   - [ ] Routing updates

2. [ ] Proxmox cluster formation
   - [ ] Initial setup on existing node
   - [ ] Join T440 to cluster
   - [ ] Verify cluster quorum

3. [ ] Storage configuration
   - [ ] Configure shared storage
   - [ ] Verify storage access from both nodes

4. [ ] Core services deployment
   - [ ] Deploy Docker hosts
   - [ ] Deploy Traefik
   - [ ] Deploy Authentik
   - [ ] Set up monitoring

5. [ ] AI services deployment
   - [ ] Deploy OpenWebUI
   - [ ] Configure integrations

## Post-Deployment Verification

- [ ] All services are running
- [ ] All services are accessible
- [ ] Monitoring is active and reporting
- [ ] Backups are configured and working
- [ ] Documentation has been updated

## Rollback Plan

- In case of failure during network changes:
  - [ ] Execute `ansible-playbook ansible/playbooks/rollback/network-rollback.yml`

- In case of failure during Proxmox integration:
  - [ ] Execute `ansible-playbook ansible/playbooks/rollback/proxmox-rollback.yml`

- In case of failure during service deployment:
  - [ ] Execute `ansible-playbook ansible/playbooks/rollback/service-rollback.yml`
  