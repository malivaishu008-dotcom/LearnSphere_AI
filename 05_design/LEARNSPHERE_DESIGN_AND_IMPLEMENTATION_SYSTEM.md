# LearnSphere AI — Design, Technology and Implementation System

**Product:** LearnSphere AI  
**Programme identity:** MINDFORGEAI · CHATAKE INNOWORKS PVT. LTD.  
**Ownership:** © 2026 CHATAKE INNOWORKS PVT. LTD. All project rights reserved.  
**Project team:** Vaishnavi Mali (2026IT012, Team Lead); Nagweni Kumbhar (2026IT011); Aishwarya Ekanath (2026IT010)  
**Industry Guide:** Akash S. Chatake  
**Reference:** [MINDFORGEAI Internship Programme](https://internship.chatakeinnoworks.com)

This is the canonical handoff document for recreating, extending, reviewing, or hosting LearnSphere AI. It records the product intent, visual system, interaction structure, data/API design, technology decisions, security boundaries, deployment method, and roadmap. New pages must follow this document unless the team approves a replacement revision.

---

## 1. Product definition

LearnSphere AI is a private study operating system for students. It makes daily study work visible and actionable through five connected loops:

```text
Capture → Plan → Focus → Check recall → Reflect and adapt
```

The experience is deliberately calm, serious and supportive. It avoids social-feed patterns, guilt-driven streaks and unqualified promises about grades. AI is an assistant to learning practice, not an authority on academic outcomes.

### Jobs it solves

| Student need | LearnSphere response |
| --- | --- |
| “My material is scattered.” | Subject-organised notes, PDFs/books, documents, images and voice-note uploads. |
| “I do not know what to do next.” | Focused tasks, planned minutes, due dates and a next-action dashboard. |
| “I revise but cannot judge understanding.” | Active-recall MCQ practice and saved quiz results. |
| “I keep losing consistency.” | Focus logging, daily diary and a consistency signal. |
| “How can I improve?” | Explicit recommended next actions and an indicative—not formal—mark scenario. |

### Experience boundary

The current release is a local MVP. It provides a deterministic local study-coach and quiz engine; it does not claim to parse documents, transcribe voice, schedule autonomous tests, generate accurate sample papers, or provide a validated prediction model. Those capabilities are roadmap items and must be evaluated before release.

---

## 2. Brand and editorial system

### Naming

- Legal/company display: **CHATAKE INNOWORKS PVT. LTD.**
- Division display: **MINDFORGEAI**
- Product display: **LearnSphere AI**
- Hero attribution: **MINDFORGEAI · CHATAKE INNOWORKS PVT. LTD.**
- Rights line: **© 2026 CHATAKE INNOWORKS PVT. LTD. All project rights reserved.**

Use the uppercase form for legal, header attribution, footer and rights contexts. In normal paragraph prose, `CHATAKE INNOWORKS PVT. LTD.` remains preferred for consistency. Do not use `Chatake`, `CHATake`, or inconsistent variations in interface copy.

### Voice

The voice is clear, calm, disciplined and practical. It treats learners as capable people. Use short action-led labels such as “Plan focused work”, “Capture what matters”, and “Make the next week smarter.” Avoid “guarantee”, “topper”, “perfect”, “failure”, or any claim that an AI result is certain.

### Brand hierarchy

```text
CHATAKE INNOWORKS PVT. LTD.  → parent/company
MINDFORGEAI                  → internship/engineering division
LearnSphere AI               → student product
```

The parent and division identify ownership and context; LearnSphere remains the primary product name in product UI.

---

## 3. Visual design system

### Colour tokens

| Token | Value | Use |
| --- | --- | --- |
| Ink | `#0A1024` | Navigation, primary controls, high-emphasis text, guide card |
| Paper | `#F6F6F1` | Main page background |
| Lime | `#B7FF5B` | Positive progress, active accents, arrow highlights |
| Violet | `#8B5CF6` | AI/intelligence accents, indicators and scores |
| Muted | `#7B7D8A` | Supporting labels and low-emphasis copy |
| Line | `#DFE0DA` | Borders and structural dividers |
| Card | `#FFFFFF` | Workspace cards and form surfaces |

Use colour to establish hierarchy—not to encode information alone. Text and status must remain readable without colour vision. The UI uses dark ink for seriousness, warm paper to reduce visual fatigue, violet to signal intelligence, and lime sparingly to signal forward motion.

### Typography

| Role | Typeface | Weight / treatment |
| --- | --- | --- |
| Product/UI | Manrope | 400–800; bold for actions and section headings |
| Metadata | DM Mono | 400–500; uppercase with 1.1px tracking |
| Hero | Manrope | 700–800; `clamp(52px, 8.5vw, 112px)`; tight negative tracking |
| Workspace title | Manrope | 700–800; 36px desktop / 29px mobile |
| Body | Manrope | 14–17px; line height 1.55–1.7 |

Fonts are loaded from Google Fonts in the landing document. For a production privacy review or offline mode, self-host approved font files and preserve the same fallback stack: `Manrope, Arial, sans-serif`.

### Shape, spacing and motion

- Navigation and cards use 8–18px radii; avoid excessive pills.
- Desktop content width: 1220px for marketing; 1300px workspace maximum.
- Default section rhythm: 112px vertical desktop, 72px mobile.
- Primary button: ink background, white text, lime arrow and 5px dark offset shadow.
- Motion is minimal: `0.25s` opacity/translation toast transition; avoid autoplay, parallax or distraction.
- Maintain visible keyboard focus (`outline-color: violet`) and semantic labels.

### Favicon and preview

`frontend/assets/favicon.svg` is an original vector: deep-ink rounded square, lime L geometry and violet bar. The HTML includes title, description, Open Graph title/description/type and theme colour. Before public release, add a deployed absolute `og:image` plus 180×180/192×192/512×512 PNG application icons.

---

## 4. Information architecture and page structure

### Public landing page

```text
Header
 ├─ LearnSphere AI mark
 ├─ System / Workflow / Trust / People anchors
 ├─ Sign in
 └─ Start studying
Hero
 ├─ MINDFORGEAI · CHATAKE INNOWORKS PVT. LTD. attribution
 ├─ Product promise and primary action
 └─ Study pulse illustration
System
 ├─ Command centre
 ├─ Personal knowledge base
 ├─ Practice engine
 └─ Learning intelligence
Workflow: Capture → Focus → Check → Adapt
Trust and AI boundaries
Project team and Industry Guide
Footer: internship, company, rights reserved
```

### Authentication surfaces

The landing page opens a full-screen auth overlay rather than sending users to visually disconnected pages.

- **Sign in:** email + password, existing-user message.
- **Create account:** name + email + minimum 8-character password, calm onboarding message.
- **On success:** store JWT and profile in browser local storage, open workspace, seed three example subjects/tasks/note for new accounts.
- **Error state:** a small toast explains validation, duplicate account or incorrect credentials.
- **Production change:** replace browser token storage with an audited secure cookie/session strategy if the threat model requires it; add rate limiting, email verification, reset-password flow, consent and terms.

### Student workspace

| View | Purpose | Current capability | Later capability |
| --- | --- | --- | --- |
| Overview | one screen for the study day | metrics, next tasks, subjects, coach, diary entry point | charts, notifications, calendar events |
| Study planner | decide what to do next | subjects, tasks, target date, focus minutes, completion | calendar/timetable drag-drop, repetition and reminders |
| Knowledge base | collect personal learning material | notes and file upload metadata | PDF extraction, OCR, citations, voice transcription, mind maps |
| Practice lab | check recall | local 3-question MCQ generation and result saving | source-grounded quizzes, surprise-test scheduler, sample papers |
| Learning insights | turn activity into action | consistency, indicative score scenario, advice | calibrated model, subject-specific trends, uncertainty charts |
| Daily diary | make study reflection visible | mood and daily reflection | weekly review synthesis, private exports |
| AI connections | explain provider boundary | provider roadmap/status cards | consent, OAuth/API provider adapters and provider controls |

### Team and company page content

The public `People` section contains:

- **Vaishnavi Mali — 2026IT012 — Team Lead**
- **Nagweni Kumbhar — 2026IT011**
- **Aishwarya Ekanath — 2026IT010**
- **Industry Guide: Akash S. Chatake**
- Official link: `https://internship.chatakeinnoworks.com`
- Rights notice: **© 2026 CHATAKE INNOWORKS PVT. LTD. All project rights reserved.**

For a future separate About page, reuse this exact order and wording; include internship story, programme context, project scope, guide attribution, team cards, rights policy and external contact links. Do not publish personal phone numbers or private student records.

---

## 5. Application technology

```text
Browser SPA (HTML + CSS + JavaScript)
        │ HTTPS / JSON / multipart upload
Flask REST application + JWT middleware
        ├─ SQLite (local MVP)
        ├─ protected local upload directory (local MVP)
        └─ AI provider adapter boundary (future)
```

### Repository locations

| Path | Responsibility |
| --- | --- |
| `06_code/frontend/index.html` | Public landing, auth overlay and workspace shell |
| `06_code/frontend/assets/app.css` | Core responsive visual system |
| `06_code/frontend/assets/app.js` | SPA state, API calls and view rendering |
| `06_code/frontend/assets/favicon.svg` | Product favicon |
| `06_code/backend/app.py` | Flask routes, database access, auth, uploads and health |
| `06_code/database/schema.sql` | Local database schema |
| `06_code/storage/uploads` | ignored local upload storage |
| `08_testing/test_api.py` | API smoke tests |
| `11_deployment` | Docker, Compose, Render configuration and guide |

### Dependencies

- Flask 3.x
- Flask-Cors 4–6.x
- Flask-JWT-Extended 4.x
- Gunicorn for Linux deployment
- SQLite is bundled with Python for the local MVP

No frontend framework is used in the initial release. This keeps the demo fast and reduces build complexity. When the product needs larger teams, component tests, complex calendar state or server rendering, move the frontend deliberately to Next.js/React or a similarly approved stack—without changing the API contract casually.

---

## 6. Data model and API contract

### Data model

| Entity | Important fields | Purpose |
| --- | --- | --- |
| `users` | name, email, password hash, created time | student identity |
| `subjects` | user, name, description, colour | student learning map |
| `tasks` | subject, title, due date, planned minutes, status | study planning |
| `notes` | subject, title, body, timestamps | student-created written knowledge |
| `resources` | subject, title, stored filename, MIME type | uploaded material metadata |
| `study_sessions` | subject, minutes, start time | focus record |
| `diary_entries` | date, mood, reflection | self-reflection loop |
| `quizzes` | topic, score, total | practice history |

Every student-owned table carries `user_id`. All workspace API routes require a JWT. SQLite foreign keys are enabled for each connection.

### Endpoint map

| Method + route | Function |
| --- | --- |
| `POST /api/auth/register` | account creation and example workspace seed |
| `POST /api/auth/login` | credential login and JWT issuance |
| `GET /api/me` | current profile |
| `GET /api/dashboard` | metrics, tasks, subjects and recent quiz |
| `GET/POST /api/subjects` | subject list and creation |
| `GET/POST/PATCH /api/tasks` | tasks and completion status |
| `GET/POST /api/notes` | student notes |
| `GET/POST /api/diary` | diary entries |
| `GET/POST /api/resources` | resource list / multipart upload |
| `POST /api/study-sessions` | focus minutes |
| `POST /api/quizzes/generate` | local practice questions |
| `POST /api/quizzes/submit` | quiz result persistence |
| `GET /api/insights` | consistency and indicative study scenario |
| `POST /api/chat` | local study-coach fallback |
| `GET /api/integrations` | AI provider roadmap/status |
| `GET /api/health` | unauthenticated service health |

---

## 7. Security, privacy and AI rules

1. Never ask a student to provide ChatGPT, Google, Gemini, NotebookLM or any third-party password.
2. AI providers must be connected only with administrator-managed server secrets or official OAuth, with least-privilege scopes.
3. Before external processing, show what student material will leave the platform and record consent.
4. The MVP allowlists upload extensions and caps size at 25 MB. Production needs authenticated downloads, malware scanning, content validation, rate limits and private object storage.
5. JWT signing secret is an environment variable. Replace the development fallback before any public deployment; never commit `.env` files.
6. CORS must name exact deployed origins in production; do not leave wildcard origin settings for a public service.
7. Predictions are learning signals only. Use “indicative”, show limitations, and never make academic, medical, financial or disciplinary decisions from them.
8. AI-generated material requires source grounding, citations where sources are used, evaluation data, prompt-injection testing and a student-report mechanism before release.

---

## 8. Local development, testing and deployment

### Local run

```powershell
cd 06_code
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python backend\app.py
```

Open `http://localhost:5000`. In the current workspace port 5000 was occupied, so the verified running instance used `http://localhost:5050`.

### Tests

```powershell
python -m unittest discover -s 08_testing -v
```

The smoke suite verifies unauthorized access rejection, registration, workspace seeding, task creation, note saving and insight response. CI runs this on Python 3.12 through GitHub Actions.

### Container package

```powershell
$env:JWT_SECRET_KEY = "long-unique-secret"
docker compose -f 11_deployment/docker-compose.yml up --build
```

### AWS/subdomain hand-off

When CHATAKE INNOWORKS PVT. LTD. allocates AWS and the subdomain:

1. Select the deployment path: ECS Fargate/App Runner is preferred for the container; Elastic Beanstalk is an acceptable simpler managed route.
2. Replace SQLite with RDS PostgreSQL and run managed migrations.
3. Replace local uploads with an encrypted private S3 bucket, per-user authorization and scanning.
4. Store `JWT_SECRET_KEY`, provider credentials and database credentials in AWS Secrets Manager or Parameter Store.
5. Put the service behind an ALB/CloudFront as appropriate, issue TLS with ACM, and create a Route 53 alias for the allocated subdomain.
6. Set `CORS_ORIGINS=https://<allocated-subdomain>` and `FLASK_DEBUG=0`.
7. Configure backups, logging/alerts, uptime health checks using `/api/health`, retention controls and an incident owner.
8. Complete privacy, security, AI evaluation and accessibility review before exposing student uploads to real users.

---

## 9. Git delivery standard

`main` is protected. Work on one branch per concern: `feature/frontend-*`, `feature/platform-*`, or `feature/aiml-*`. A merge requires a peer review, passing tests, no private/student material, no secret, a concise change summary and rollback note.

The existing repository is initialized and has these baseline commits:

```text
465e388 feat: establish LearnSphere AI study platform MVP
fa3e874 fix: close database connections and verify local runtime
3cd65e3 chore: add service health endpoint
```

To publish after a CHATAKE-owned remote repository is created and access is granted:

```powershell
git remote add origin <approved-repository-url>
git branch -M main
git push -u origin main
```

Do not use a personal repository for company-owned work unless CHATAKE INNOWORKS PVT. LTD. explicitly approves it.

---

## 10. Extension rules and roadmap

### Next pages

1. **About / Team page:** company hierarchy, team, guide, internship link, rights.
2. **Resource detail page:** document viewer, source metadata, consent and delete/download controls.
3. **Timetable page:** time blocks, recurring schedules and clear conflict behaviour.
4. **Practice detail page:** question source, rationale, progress and retest cycle.
5. **Insights detail page:** transparent calculation, confidence and actionable intervention.
6. **Settings page:** account controls, data export/deletion, integration consent and notification settings.

### Delivery phases

| Phase | Outcome |
| --- | --- |
| 1 — foundation | current persistent MVP, landing, workspace, tests and deployment package |
| 2 — content intelligence | PDF/OCR pipeline, private storage, citations and evaluated RAG |
| 3 — practice intelligence | syllabus mapping, validated quizzes, sample papers and careful notifications |
| 4 — learning analytics | calibrated signals, cohort-free personal trends and transparent explanations |
| 5 — pilot and scale | consented pilot, outcomes study, AWS hosting, monitoring and operational support |

Every addition must preserve student agency, clear source/AI provenance, mobile usability, accessibility, secure data separation and the design language defined above.
