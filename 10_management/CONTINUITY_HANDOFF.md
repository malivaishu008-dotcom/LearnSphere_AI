# LearnSphere AI — Continuity Handoff

**Last updated:** 2026-08-07  
**Owner:** MINDFORGEAI · CHATAKE INNOWORKS PVT. LTD.  
**Purpose:** This document enables a new Codex/chat session or team member to continue the project safely without rediscovering the architecture, current status, or deployment constraints.

## Current delivery state

| Area | Status | Evidence |
| --- | --- | --- |
| Local MVP | Complete and running | `http://localhost:5050` in this workspace |
| API verification | Passing | `python -m unittest discover -s 08_testing -v` — 2 tests pass |
| Service health | Passing | `GET /api/health` returns 200 JSON |
| Git history | Committed | current baseline commit `dad0c38` |
| Remote Git hosting | Blocked by missing target | no `origin` remote; GitHub CLI is not installed/authenticated |
| AWS/subdomain deployment | Awaiting company allocation | no AWS account credentials, target region, subdomain or DNS zone supplied |

## Exact repository location

```text
D:\itr\project\ML-EDU-06_LearnSphere_AI
```

## Essential documents

1. `05_design/LEARNSPHERE_DESIGN_AND_IMPLEMENTATION_SYSTEM.md` — canonical design, architecture, page and deployment specification.
2. `11_deployment/DEPLOYMENT.md` — local, Docker, Render and readiness guide.
3. `11_deployment/AWS_RELEASE_RUNBOOK.md` — AWS implementation sequence and go/no-go gate.
4. `01_project_definition/PRODUCT_BLUEPRINT.md` — scope, product thesis and roadmap.
5. `10_management/TEAM_WORKPLAN.md` — three-person ownership and Git workflow.
6. `AGENTS.md` — durable engineering and safety rules for coding agents.

## Current platform implementation

- **Frontend:** responsive HTML/CSS/JavaScript SPA in `06_code/frontend`.
- **Backend:** Flask API in `06_code/backend/app.py`.
- **Persistence:** SQLite local MVP at `06_code/database/learnsphere.db`, ignored by Git.
- **Uploads:** local private directory at `06_code/storage/uploads`, ignored by Git.
- **Auth:** JWT bearer access to student-owned API routes.
- **Core flows:** account access, subjects, tasks, notes, uploads, focus sessions, diary, simple quizzes, local coach fallback, insights, health endpoint.
- **Brand:** `MINDFORGEAI · CHATAKE INNOWORKS PVT. LTD.`; all project rights reserved by CHATAKE INNOWORKS PVT. LTD.

## What is intentionally not yet production-ready

- SQLite/local uploads must become PostgreSQL/S3 or another private object store.
- Gemini is configured only with a server-side `GEMINI_API_KEY`; do not solicit student passwords. NotebookLM remains an external workspace link.
- No document extraction/RAG, OCR, transcription, scheduled surprise tests or validated prediction model.
- No email verification, password reset, rate limiting, malware scan, user deletion/export, monitoring or legal privacy process.
- Do not publicly deploy student uploads before these are handled.

## Immediate next actions for a new session

1. Read the design system and AWS release runbook completely.
2. Inspect `git status --short` and `git log --oneline -5`; preserve any user changes.
3. Verify locally:

   ```powershell
   $py='C:\Users\nagwe\AppData\Local\Programs\Python\Python312\python.exe'
   & $py -m unittest discover -s 08_testing -v
   Invoke-WebRequest http://localhost:5050/api/health -UseBasicParsing
   ```

4. Obtain the approved CHATAKE Git remote URL. Then run:

   ```powershell
   git remote add origin <approved-url>
   git branch -M main
   git push -u origin main
   ```

5. Obtain AWS account ID, region, deployment owner, allocated subdomain, Route 53/DNS control, container registry choice, database policy and secret-management access.
6. Follow the AWS runbook. Do not bypass its go/no-go gate.

## Deployment decision

Use containerised Flask on **AWS App Runner** for the first supervised pilot, unless CHATAKE allocates ECS/Fargate as its standard. App Runner reduces operations while retaining a Docker-based build. Use RDS PostgreSQL and private S3 before public or student-data use. Attach the company subdomain only after TLS, health checks and CORS are configured.

## Git baseline

```text
dad0c38 docs: establish CHATAKE design system and project attribution
3cd65e3 chore: add service health endpoint
fa3e874 fix: close database connections and verify local runtime
465e388 feat: establish LearnSphere AI study platform MVP
```

## Non-negotiable safety rules

- Do not commit `.env`, SQLite databases, upload content, access tokens or student data.
- Do not request personal external-provider passwords.
- Keep mark predictions labelled indicative with limitations.
- Keep CHATAKE INNOWORKS PVT. LTD. rights and MINDFORGEAI attribution on public materials.
- Run the test suite before committing or deployment.
