# AWS Release Runbook — LearnSphere AI

**Release owner:** CHATAKE INNOWORKS PVT. LTD.  
**Recommended first managed runtime:** AWS App Runner  
**Alternative:** ECS Fargate if the company already operates an ECS platform

## Preconditions — obtain before any cloud action

- Approved CHATAKE-owned Git remote and repository access.
- AWS account, deployment region and named deployment owner.
- Allocated subdomain and authority to update its DNS/Route 53 record.
- Decision on PostgreSQL (RDS) and private file storage (S3) ownership/retention.
- AWS Secrets Manager or Parameter Store access.
- Privacy/data handling approval for the intended pilot audience.

## Target architecture

```text
Student browser
  → HTTPS + allocated subdomain
  → Route 53 / ACM certificate
  → AWS App Runner service (container)
      → RDS PostgreSQL (private network)
      → S3 private bucket (student uploads)
      → Secrets Manager (JWT and provider secrets)
      → CloudWatch logs, alarms and health checks
```

## Deployment sequence

1. **Publish source.** Push the reviewed `main` branch to the CHATAKE-owned remote. Enable protected branches and the existing GitHub Actions test workflow.
2. **Build image.** Create an ECR repository (for example `learnsphere-ai`) and build from `11_deployment/Dockerfile`. Scan the image and tag it with the immutable commit SHA.
3. **Provision data.** Create a private RDS PostgreSQL instance, backups, least-privilege application user and a migration approach. Do not carry the local SQLite database into production.
4. **Provision files.** Create a private S3 bucket with encryption, lifecycle rules, restricted IAM role and malware-scanning workflow. Replace local upload code with signed/authorised S3 storage before student uploads are accepted.
5. **Create secrets.** Store a long random `JWT_SECRET_KEY`, database URL and any approved AI-provider key in Secrets Manager. Never put them in Git, a Docker image or browser JavaScript.
6. **Deploy runtime.** Configure App Runner with the ECR image, port `5000`, `FLASK_DEBUG=0`, exact production `CORS_ORIGINS`, secret references and `/api/health` health check.
7. **Attach domain.** Request/validate ACM certificate, attach the allocated subdomain in App Runner or CloudFront, create the DNS alias, and verify HTTPS redirect/certificate validity.
8. **Observe.** Configure CloudWatch retention, 5xx/latency alarms, health failure alarm, budget alert and an incident contact.
9. **Pilot only.** Execute a supervised test account flow, data separation test, upload validation test, logout test and deletion/export procedure before inviting students.

## Required application changes before real student data

| Requirement | Why | Status |
| --- | --- | --- |
| PostgreSQL repository/migrations | concurrency, backup and managed durability | pending |
| S3 private upload adapter | durable protected file handling | pending |
| authenticated download and antivirus scanning | upload safety | pending |
| email verification/reset + rate limits | account protection | pending |
| consent, privacy notice, export/deletion | student-data governance | pending |
| provider adapter with audit/evaluation | safe AI connection | pending |
| error monitoring and metrics | operational support | pending |

## Go / no-go gate

Do **not** attach the public subdomain or accept real student data until each is checked:

- [ ] Source is in the CHATAKE-owned remote; tests and review are passing.
- [ ] TLS, exact CORS, non-debug mode and secret management are active.
- [ ] RDS backup/restore is exercised; local SQLite is not production storage.
- [ ] S3 is private, encrypted, authorised and scanned.
- [ ] Privacy consent, deletion/export and incident ownership are documented.
- [ ] AI calls are consented, source-grounded, evaluated and never use student passwords.
- [ ] Security, accessibility and mobile acceptance test evidence is signed off.

## Rollback

Use immutable container tags. On a regression, redeploy the prior passing image, keep database migrations backward-compatible, and never roll back by deleting/overwriting student data. Record the incident, affected version, owner and user impact.
