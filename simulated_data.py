# Simulated threat data from different sources

HORIZON3_THREAT = {
    "source": "Horizon3.ai",
    "finding_id": "H3-CVE-2025-12345",
    "severity": "CRITICAL",
    "host": "srv-finance-01.yourcompany.local",
    "ip_address": "10.1.10.55",
    "vulnerability": "Critical RCE in ObsoleteApp v1.2",
    "description": "Remote code execution vulnerability allows attackers to execute arbitrary commands",
    "cvss_score": 9.8,
    "timestamp": "2025-01-19T10:30:00Z",
    "affected_service": "ObsoleteApp",
    "port": 8080
}

BRIGHT_DATA_THREAT = {
    "source": "Bright Data",
    "alert_id": "BD-MALWARE-2025-001",
    "severity": "HIGH", 
    "host": "web-server-02.yourcompany.local",
    "ip_address": "192.168.1.100",
    "threat_type": "Malware Detection",
    "description": "Suspicious executable detected attempting network communication",
    "confidence": 0.85,
    "timestamp": "2025-01-19T11:15:00Z",
    "file_hash": "a1b2c3d4e5f6789012345678901234567890abcd",
    "process_name": "suspicious_process.exe"
}

# Additional test cases
TEST_THREATS = [
    {
        "source": "Internal Scanner",
        "alert_id": "IS-VULN-2025-003",
        "severity": "MEDIUM",
        "host": "db-server-01.yourcompany.local", 
        "ip_address": "10.0.0.50",
        "vulnerability": "Outdated SSL Certificate",
        "description": "SSL certificate expired 30 days ago",
        "timestamp": "2025-01-19T09:45:00Z"
    }
]
