# LearnSphere AI

LearnSphere AI is a student-centred study operating system developed during the **MindForgeAI AIML Internship** at **Chatake Innoworks Pvt. Ltd.** It gives students a focused workspace for subjects, plans, notes, syllabus, timetable, previous-year questions, uploads, practice, diary reflections, and learning signals.

The project is designed as a responsible AIML internship deliverable. AI support is framed as study assistance, not authority. Any predicted mark is an indicative learning scenario only and must not be treated as certain, diagnostic, or official.

## Current Status

This repository now contains a runnable full-stack MVP, modern branded frontend, Flask backend, SQLite persistence, tests, deployment assets, and complete academic documentation.

## Run Locally

```powershell
cd 06_code
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python backend\app.py
```

Open `http://localhost:5000`.

## Deploy the Application API

GitHub Pages hosts the project website. To enable account creation and sign-in on that website, deploy the Flask API through [Render](https://render.com/deploy?repo=https%3A%2F%2Fgithub.com%2FEkanath2417%2FLearnSphere_AI). The current API deployment is `https://learnsphere-ai-c01p.onrender.com`.

## What Is Included

- Branded landing page for LearnSphere AI with Chatake Innoworks / MindForgeAI attribution.
- Student registration, login, dashboard, subjects, tasks, focus logging, diary, quizzes, and insights.
- Academic library modules for notes, syllabus, previous-year questions, and timetable records.
- Upload support for learning resources in the local MVP.
- Provider-neutral AI connection policy that never asks students for third-party passwords.
- Docker, Render, GitHub Actions, deployment guidance, and project reports.

## Repository Map

| Folder | Purpose |
| --- | --- |
| `01_project_definition` | Product blueprint, scope, and master build prompt |
| `02_research_and_sources` | Research and brand reference log |
| `03_data_and_resources` | Data/resource holding area |
| `04_active_workspace` | Working area for team activity |
| `05_design` | Design and implementation system |
| `06_code` | Flask backend, frontend, database schema, requirements |
| `07_models_and_artifacts` | AIML module stubs and future model areas |
| `08_testing` | Automated API tests |
| `09_project_diaries` | Project diary space |
| `10_management` | Team plan and hand-off documentation |
| `11_deployment` | Docker, Render, AWS, and GitHub hosting guides |
| `12_presentation_and_demo` | Abstract, reports, literature survey, conclusion, and final report |

## Documentation Pack

- `12_presentation_and_demo/ABSTRACT.md`
- `12_presentation_and_demo/ACADEMIC_REPORT.md`
- `12_presentation_and_demo/LITERATURE_SURVEY.md`
- `12_presentation_and_demo/CONCLUSION.md`
- `12_presentation_and_demo/FINAL_REPORT.md`
- `12_presentation_and_demo/INDUSTRY_REPORT.md`
- `11_deployment/DEPLOYMENT.md`
- `11_deployment/GITHUB_PAGES.md`

## Testing

Run the required hand-off test suite from the repository root:

```powershell
python -m unittest discover -s 08_testing
```

## Deployment Notes

The local MVP uses SQLite and local uploads for simple demonstration. Before public production deployment, move to PostgreSQL and private object storage, configure HTTPS, use a strong `JWT_SECRET_KEY`, restrict CORS origins, add rate limits, scan uploads, create backups, and complete a privacy review.

The static landing page can be hosted through GitHub Pages. The full logged-in web application needs the Flask backend running on a platform such as Render, AWS, or another approved host.

## Branding

LearnSphere AI is an internship project under Chatake Innoworks Pvt. Ltd. / MindForgeAI Division. The product identity is distinct while being aligned with the organisation's research-driven engineering-learning environment.
