# Academic Project Report - LearnSphere AI

## Title

LearnSphere AI: A Student-Centred Study Operating System for Planning, Practice, Reflection, and Responsible Learning Signals

## Abstract

LearnSphere AI is a full-stack academic productivity web application developed during the MindForgeAI AIML Internship at Chatake Innoworks Pvt. Ltd. The project addresses a common student problem: academic work is scattered across notebooks, PDFs, class timetables, previous-year papers, reminder apps, and disconnected AI tools. LearnSphere AI consolidates these activities into one focused workspace where students can create accounts, manage subjects, plan tasks, store notes, maintain syllabus and timetable records, practise short quizzes, upload learning resources, log focus sessions, write diary reflections, and review clearly labelled learning signals.

The system uses a Flask backend, SQLite database for the local MVP, JWT-protected student workspace endpoints, modular academic-content APIs, and a responsive HTML/CSS/JavaScript frontend. The application intentionally treats AI as supportive study assistance, not as an authority. Predicted marks are presented only as indicative scenarios and are never claimed to be certain or diagnostic. The project also follows a privacy-aware integration approach: students must not be asked for third-party provider passwords, and future AI provider access should use server-side secrets or approved OAuth flows.

## Chapter 1 - Introduction

Students often have access to many learning materials but lack a practical operating system for converting those materials into daily action. A student may have lecture notes in one place, PDFs in another, timetable information elsewhere, and exam questions in a separate folder. This fragmentation increases cognitive load and makes it difficult to answer a simple question: what should I study next?

LearnSphere AI is designed as a calm study operating system. Instead of competing for attention, it helps the student organise academic work into a loop: capture, plan, practise, reflect, and adapt. The application is especially suitable as an internship project because it combines web development, backend APIs, database modelling, product design, software testing, deployment preparation, and responsible AIML thinking.

## Chapter 2 - Problem Statement

Many students do not fail to study because they lack material; they struggle because the material is scattered, revision is not planned, and feedback arrives too late. Conventional learning-management systems mainly distribute content, while personal productivity tools often ignore academic context. AI tools can help explain concepts, but when used without structure, they may introduce privacy risks, unreliable outputs, or unrealistic expectations.

The problem is to design and implement a student-focused web application that brings academic planning, resources, practice, reflection, and safe learning intelligence into one usable system.

## Chapter 3 - Objectives

1. Build a clean, responsive web application for students.
2. Provide authenticated student workspaces for personal planning and activity tracking.
3. Support subjects, study tasks, notes, timetable, syllabus, previous-year questions, resources, quizzes, focus sessions, and diary entries.
4. Integrate backend APIs with the frontend experience.
5. Keep AI and prediction language supportive, transparent, and non-diagnostic.
6. Prepare deployment assets, documentation, tests, and GitHub hosting guidance.

## Chapter 4 - Literature Survey

Educational technology research frequently highlights the importance of self-regulated learning, retrieval practice, spaced revision, reflection, and timely feedback. LearnSphere AI draws from these directions and converts them into practical software modules.

Self-regulated learning suggests that students improve when they can set goals, monitor effort, and adapt strategies. This motivates the dashboard, planner, focus logging, and diary. Retrieval practice research supports active recall rather than passive rereading, which motivates the practice lab and quiz flow. Learning analytics can help students notice patterns, but analytics must be presented carefully so students are not misled. This motivates the system's "indicative only" language for mark scenarios.

The project also responds to privacy and AI safety concerns. Modern AI-enabled education systems should avoid collecting unrelated credentials, should explain when external providers are used, and should maintain a non-AI fallback where possible. LearnSphere AI therefore keeps the MVP provider-neutral and documents a safer production integration route.

## Chapter 5 - System Analysis

### Existing workflow issues

- Notes, syllabus, timetable, and question papers are usually stored separately.
- Students may plan tasks without connecting them to actual study resources.
- Revision often becomes last-minute because recall checks are not built into the workflow.
- Students may over-trust AI-generated explanations or predicted marks if limitations are not visible.

### Proposed system

LearnSphere AI centralises academic work inside a single web application. The public landing page introduces the product, internship context, and trust principles. After login, the student workspace provides dashboard, planner, knowledge base, syllabus, previous questions, timetable, practice lab, learning insights, diary, and AI connection guidance.

## Chapter 6 - System Design

### Architecture

- Frontend: responsive single-page interface using HTML, CSS, and JavaScript.
- Backend: Flask REST API.
- Authentication: JWT for personal workspace endpoints.
- Database: SQLite for local demonstration.
- ORM modules: SQLAlchemy models and services for academic content.
- Deployment: Docker, Render starter configuration, GitHub Actions testing, and GitHub Pages landing-page guidance.

### Main modules

| Module | Description |
| --- | --- |
| Authentication | Register, login, and retrieve current user |
| Dashboard | Study metrics, next actions, subjects, and coach panel |
| Planner | Subjects and task planning |
| Knowledge base | Notes and academic material capture |
| Syllabus | Course unit records |
| Previous questions | PYQ question bank records |
| Timetable | Weekly class/study timetable |
| Practice lab | Short active-recall quiz generation and scoring |
| Insights | Consistency and indicative mark scenario |
| Diary | Daily reflection records |
| Integrations | Safe AI provider roadmap |

## Chapter 7 - Implementation

The backend is implemented in `06_code/backend`. The main Flask app initialises the database, serves the frontend, exposes protected student APIs, registers modular academic blueprints, handles uploads, and returns consistent JSON responses. SQL schema and runtime database files are stored under `06_code/database`, while local uploads are kept under `06_code/storage/uploads` and excluded from git except for a `.gitkeep` placeholder.

The frontend is implemented in `06_code/frontend`. It provides a branded landing page and a dynamic student workspace. JavaScript connects each view to its API endpoint and renders state without a build system, keeping the internship demonstration simple and easy to run.

## Chapter 8 - Testing

Automated tests are stored in `08_testing`. They verify:

- Account registration and JWT-protected access.
- Dashboard availability.
- Task creation.
- Note creation.
- Insight response.
- Academic content CRUD flows.
- PDF upload validation for academic material.
- Timetable validation.

The required hand-off command is:

```powershell
python -m unittest discover -s 08_testing
```

## Chapter 9 - Deployment

The project can run locally with Python and can be packaged with Docker. `11_deployment/render.yaml` provides a starter managed-hosting configuration. For public production use, the project should move from SQLite/local uploads to PostgreSQL/private object storage, add HTTPS, rate limiting, malware scanning, monitoring, backups, and a privacy review.

The static landing page can also be published to GitHub Pages for project presentation. The full application still needs the Flask backend for login and workspace features.

## Chapter 10 - Results

The project has been transformed into a coherent deployable MVP with:

- Branded landing page and footer referencing Chatake Innoworks Pvt. Ltd. and MindForgeAI.
- Modern responsive student workspace.
- Integrated frontend/backend workflows.
- Academic content modules.
- Deployment configuration.
- CI test workflow.
- Complete documentation and reports.

## Chapter 11 - Limitations

- SQLite and local uploads are suitable for demos, not multi-user public production.
- The quiz generator is a starter local practice engine, not a fully evaluated subject-grounded AI system.
- Uploaded documents are stored but not yet parsed into a retrieval pipeline.
- Academic APIs currently support demo-friendly shared content behaviour; production should enforce per-user ownership consistently.
- Any mark scenario is indicative only and must not be treated as certain or diagnostic.

## Chapter 12 - Future Scope

1. PostgreSQL migration and data backup strategy.
2. Private object storage and secure file downloads.
3. Document extraction, embeddings, and citation-backed retrieval.
4. Evaluated quiz generation mapped to syllabus units.
5. Calendar reminders and optional notification scheduling.
6. Student data export and deletion.
7. Accessibility audit and mobile usability testing.
8. Consented pilot study with clear outcome measures.

## Conclusion

LearnSphere AI demonstrates how a student-centred study application can combine practical full-stack engineering with responsible AIML design. The system does not promise automatic academic improvement; instead, it creates a clearer environment for planning, practice, reflection, and informed next actions. With production-grade storage, evaluated AI pipelines, and a privacy review, it can become a strong pilot-ready educational technology platform.
