# Company Asset Inventory

## Critical Servers

### srv-finance-01 (10.1.10.55)
- **Department**: Finance
- **Criticality**: CRITICAL
- **Function**: Processes quarterly earnings reports and contains employee PII
- **System Owner**: Alice (alice@yourcompany.com)
- **Business Impact**: High - Contains sensitive financial data and personal information
- **Backup Schedule**: Daily at 2 AM
- **Maintenance Window**: Sundays 2-6 AM

### web-server-02 (192.168.1.100)  
- **Department**: IT/Web Services
- **Criticality**: HIGH
- **Function**: Public-facing web server hosting company website
- **System Owner**: Bob (bob@yourcompany.com)
- **Business Impact**: Medium - Customer-facing service
- **Load Balancer**: Yes, can handle traffic during maintenance

### db-server-01 (10.0.0.50)
- **Department**: IT/Database Services
- **Criticality**: HIGH
- **Function**: Primary customer database server
- **System Owner**: Carol (carol@yourcompany.com)  
- **Business Impact**: High - Customer data and transactions
- **Replication**: Master-slave setup with db-server-02

## Security Policies

### Incident Response Contacts
- **Security Team**: security@yourcompany.com
- **On-call Engineer**: +1-555-0123
- **CISO**: Jane Smith (jane.smith@yourcompany.com)

### Escalation Matrix
- **Low Severity**: Ticket only
- **Medium Severity**: Email + Slack notification
- **High Severity**: Phone call + Email + Slack
- **Critical Severity**: Immediate phone call + All hands notification

### Approved Actions
- **isolate_host**: Automatically approved for CRITICAL threats
- **patch_system**: Requires change management approval unless CRITICAL
- **reset_credentials**: Automatically approved for credential compromise
- **monitor_closely**: Always approved
- **emergency_shutdown**: Requires CISO approval unless imminent data breach

## Compliance Requirements
- **SOX Compliance**: srv-finance-01 requires 4-hour RTO
- **PCI DSS**: All customer data systems require immediate notification
- **GDPR**: Any PII-related incidents require legal team notification
