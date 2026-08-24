# Deployment Guide - LearnSphere AI

## Local Demonstration

From the repository root:

```powershell
cd 06_code
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python backend\app.py
```

Open `http://localhost:5000`.

## Environment Variables

Create `06_code/backend/.env` from `.env.example` and set:

- `JWT_SECRET_KEY` - long unique server secret.
- `CORS_ORIGINS` - exact allowed origins for the deployed frontend/API.
- `FLASK_DEBUG` - `0` for production-like runs.
- Future AI provider keys - server-side only, never in frontend code or git.

## Docker Package

```powershell
$env:JWT_SECRET_KEY = "generate-a-long-unique-secret"
docker compose -f 11_deployment/docker-compose.yml up --build
```

The Docker setup persists SQLite and uploads through volumes. It is useful for demos but not the recommended multi-user production architecture.

## Render Starter Deployment

`11_deployment/render.yaml` provides a starter web service:

- Build command: install `06_code/requirements.txt`.
- Start command: run Gunicorn against `backend.wsgi:app`.
- Health check path: `/`.

For a real pilot, attach PostgreSQL and private object storage instead of relying on ephemeral local files.

## GitHub Pages

GitHub Pages can publish the static frontend as a public project website. It cannot run the Flask backend. Use `11_deployment/GITHUB_PAGES.md` for the Pages workflow.

Recommended split:

- GitHub Pages: landing page and project presentation.
- Render/AWS/App Runner: Flask backend and full application.

## Production Readiness Gate

- [ ] PostgreSQL with migrations and backups
- [ ] Private object storage for uploads
- [ ] Upload malware scanning and file validation
- [ ] HTTPS everywhere
- [ ] Explicit CORS origins
- [ ] Rate limiting and abuse protection
- [ ] Per-user ownership for all student and academic content
- [ ] Privacy notice, consent text, deletion/export process
- [ ] AI provider review, prompt-injection tests, source citations, and evaluation
- [ ] Accessibility and mobile acceptance testing
- [ ] Monitoring, logs, alerts, and incident contact

## Rollback

Use immutable tagged releases. If a release fails, redeploy the previous passing image and preserve database/object-storage state. Do not overwrite student data during rollback.
