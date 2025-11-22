import type {
  StatsSummary,
  Finding,
  PaginatedResponse,
} from '../types';

export const MOCK_STATS_SUMMARY: StatsSummary = {
  total_events: 1234,
  total_findings: 87,
  findings_by_severity: {
    low: 25,
    medium: 30,
    high: 20,
    critical: 12,
  },
  events_over_time: [
    { date: '2025-11-15', count: 80 },
    { date: '2025-11-16', count: 95 },
    { date: '2025-11-17', count: 110 },
    { date: '2025-11-18', count: 130 },
    { date: '2025-11-19', count: 120 },
    { date: '2025-11-20', count: 140 },
    { date: '2025-11-21', count: 160 },
  ],
};

const MOCK_FINDINGS_ITEMS: Finding[] = [
  {
    id: 1,
    rule_name: 'Too many failed logins (user)',
    description:
      'User john.doe had 7 failed login attempts within 10 minutes.',
    severity: 'high',
    user: 'john.doe',
    created_at: '2025-11-21T09:23:00Z',
    risk_score: 78,
    ai_explanation:
      'Multiple failed logins may indicate a brute-force attempt or a user struggling with credentials. Consider enforcing MFA or locking the account after a threshold.',
  },
  {
    id: 2,
    rule_name: 'Repository without branch protection',
    description:
      'Repo "payments-service" has no branch protection rules for main branch.',
    severity: 'medium',
    user: 'service-owner',
    created_at: '2025-11-20T14:11:00Z',
    risk_score: 65,
    ai_explanation:
      'Lack of branch protection on production branches can lead to accidental or unreviewed changes. Enable required reviews and status checks.',
  },
  {
    id: 3,
    rule_name: 'Admin login from unusual country',
    description:
      'Admin user "security-admin" logged in from an IP located in a new country (compared to last 90 days).',
    severity: 'critical',
    user: 'security-admin',
    created_at: '2025-11-20T03:47:00Z',
    risk_score: 92,
    ai_explanation:
      'Unusual location for an admin account could indicate credential theft. Verify the session and consider forcing a password reset.',
  },
  {
    id: 4,
    rule_name: 'Public S3 bucket detected',
    description: 'S3 bucket "logs-archive-2024" is publicly accessible.',
    severity: 'high',
    user: null,
    created_at: '2025-11-19T18:05:00Z',
    risk_score: 88,
    ai_explanation:
      'Public buckets can expose sensitive data to the internet. Restrict access to the bucket or move the data to a private location.',
  },
  {
    id: 5,
    rule_name: 'Inactive user with active token',
    description:
      'User "old-contractor" is disabled but still has an active API token.',
    severity: 'medium',
    user: 'old-contractor',
    created_at: '2025-11-18T12:33:00Z',
    risk_score: 70,
    ai_explanation:
      'Disabled users should not retain active access tokens. Revoke all tokens for deactivated accounts.',
  },
  {
    id: 6,
    rule_name: 'SSH key without expiration',
    description:
      'SSH key for user "devops-team" has been active for 547 days without rotation.',
    severity: 'low',
    user: 'devops-team',
    created_at: '2025-11-18T08:22:00Z',
    risk_score: 45,
    ai_explanation:
      'Long-lived SSH keys pose a security risk. Implement key rotation policies and consider short-lived certificates.',
  },
  {
    id: 7,
    rule_name: 'Database exposed to internet',
    description:
      'Production database "customer-db-prod" has a public IP address with open port 5432.',
    severity: 'critical',
    user: null,
    created_at: '2025-11-17T22:15:00Z',
    risk_score: 95,
    ai_explanation:
      'Production databases should never be directly accessible from the internet. Place behind VPN or use private networking with bastion hosts.',
  },
  {
    id: 8,
    rule_name: 'Secrets in code repository',
    description:
      'Repository "mobile-app" contains hardcoded API keys in config files.',
    severity: 'critical',
    user: 'mobile-dev',
    created_at: '2025-11-17T16:40:00Z',
    risk_score: 90,
    ai_explanation:
      'Hardcoded secrets in repositories can be extracted by anyone with access. Remove secrets from code and use environment variables or secret management services.',
  },
  {
    id: 9,
    rule_name: 'Unpatched critical vulnerability',
    description:
      'Server "web-server-03" running software with known CVE-2024-12345 (CVSS 9.8).',
    severity: 'critical',
    user: null,
    created_at: '2025-11-17T11:30:00Z',
    risk_score: 98,
    ai_explanation:
      'Critical vulnerabilities with public exploits pose immediate risk. Patch systems urgently or isolate from network until remediation.',
  },
  {
    id: 10,
    rule_name: 'Weak password policy detected',
    description:
      'Password policy for application "internal-portal" allows passwords shorter than 8 characters.',
    severity: 'medium',
    user: null,
    created_at: '2025-11-16T19:25:00Z',
    risk_score: 62,
    ai_explanation:
      'Weak password policies increase the risk of credential compromise. Enforce minimum 12 characters with complexity requirements.',
  },
  {
    id: 11,
    rule_name: 'Excessive permissions granted',
    description:
      'User "junior-dev" has admin access to production environment.',
    severity: 'high',
    user: 'junior-dev',
    created_at: '2025-11-16T14:50:00Z',
    risk_score: 82,
    ai_explanation:
      'Principle of least privilege violated. Review and restrict access to only what is necessary for job function.',
  },
  {
    id: 12,
    rule_name: 'Backup encryption disabled',
    description:
      'Backup storage for "user-data" does not have encryption at rest enabled.',
    severity: 'high',
    user: null,
    created_at: '2025-11-16T09:18:00Z',
    risk_score: 80,
    ai_explanation:
      'Unencrypted backups can lead to data breaches if storage is compromised. Enable encryption at rest for all backup storage.',
  },
  {
    id: 13,
    rule_name: 'Missing MFA for privileged account',
    description:
      'Admin account "sys-admin-01" does not have multi-factor authentication enabled.',
    severity: 'critical',
    user: 'sys-admin-01',
    created_at: '2025-11-15T21:05:00Z',
    risk_score: 94,
    ai_explanation:
      'Privileged accounts without MFA are highly vulnerable to credential theft. Enforce MFA for all administrative access immediately.',
  },
  {
    id: 14,
    rule_name: 'Outdated TLS version in use',
    description:
      'API endpoint "api.example.com" still accepts TLS 1.0 connections.',
    severity: 'medium',
    user: null,
    created_at: '2025-11-15T16:42:00Z',
    risk_score: 58,
    ai_explanation:
      'TLS 1.0 and 1.1 have known vulnerabilities. Upgrade to TLS 1.2 or 1.3 to ensure secure communications.',
  },
  {
    id: 15,
    rule_name: 'Logging disabled for critical system',
    description:
      'Authentication service "auth-service" has audit logging turned off.',
    severity: 'high',
    user: null,
    created_at: '2025-11-15T10:28:00Z',
    risk_score: 76,
    ai_explanation:
      'Without audit logs, security incidents cannot be investigated. Enable comprehensive logging for all authentication events.',
  },
  {
    id: 16,
    rule_name: 'Default credentials detected',
    description:
      'IoT device "camera-lobby-01" using default admin password.',
    severity: 'critical',
    user: null,
    created_at: '2025-11-14T18:55:00Z',
    risk_score: 96,
    ai_explanation:
      'Default credentials are publicly known and actively exploited. Change all default passwords immediately.',
  },
  {
    id: 17,
    rule_name: 'Unnecessary service running',
    description:
      'Server "file-server-02" has Telnet service enabled and listening.',
    severity: 'medium',
    user: null,
    created_at: '2025-11-14T13:20:00Z',
    risk_score: 64,
    ai_explanation:
      'Telnet transmits data in cleartext and should be disabled. Use SSH for secure remote access instead.',
  },
  {
    id: 18,
    rule_name: 'Suspicious file download',
    description:
      'User "contractor-bob" downloaded 500MB of customer data to personal device.',
    severity: 'high',
    user: 'contractor-bob',
    created_at: '2025-11-14T08:45:00Z',
    risk_score: 85,
    ai_explanation:
      'Large data downloads to external devices may indicate data exfiltration. Investigate user activity and review data access patterns.',
  },
  {
    id: 19,
    rule_name: 'Firewall rule too permissive',
    description:
      'Firewall rule allows traffic from 0.0.0.0/0 to production database port.',
    severity: 'critical',
    user: null,
    created_at: '2025-11-13T20:30:00Z',
    risk_score: 93,
    ai_explanation:
      'Allowing traffic from anywhere defeats the purpose of a firewall. Restrict access to known, trusted IP ranges only.',
  },
  {
    id: 20,
    rule_name: 'Certificate expiring soon',
    description:
      'SSL certificate for "payment.example.com" expires in 5 days.',
    severity: 'low',
    user: null,
    created_at: '2025-11-13T15:12:00Z',
    risk_score: 50,
    ai_explanation:
      'Expired certificates cause service disruptions and browser warnings. Renew certificates before expiration and implement automated renewal.',
  },
];

export const MOCK_FINDINGS_RESPONSE: PaginatedResponse<Finding> = {
  items: MOCK_FINDINGS_ITEMS,
  total: MOCK_FINDINGS_ITEMS.length,
  page: 1,
  page_size: MOCK_FINDINGS_ITEMS.length,
};
