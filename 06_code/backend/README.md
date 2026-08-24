# LearnSphere AI Backend

The Flask backend combines the authenticated student workspace with modular academic-content APIs. SQLite is used for the local MVP so the internship demo can run without external infrastructure.

## Setup and Run

```powershell
cd 06_code
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item backend\.env.example backend\.env
python backend\app.py
```

The server listens on `http://127.0.0.1:5000`. The database is created at `06_code/database/learnsphere.db`.

## Architecture

- `app.py` - application setup, authentication, protected student APIs, frontend serving, uploads, and error handlers.
- `models/` - SQLAlchemy ORM models for notes, syllabus, PYQs, and timetable.
- `routes/` - Flask blueprints for academic-content modules.
- `services/` - reusable query and persistence operations.
- `utils/validators.py` - JSON, number, semester, and time validation.

## API Behaviour

Personal workspace endpoints such as dashboard, subjects, tasks, diary, resources, quizzes, insights, chat, and integrations require the JWT returned by login or registration.

The academic-content blueprints currently use a demo-friendly shared content scope so they can be exercised easily from the project frontend and tests. Before public production, these APIs should be aligned to authenticated per-user ownership.

## Main Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/api/auth/register` | Create student account |
| POST | `/api/auth/login` | Sign in |
| GET | `/api/me` | Current account |
| GET | `/api/dashboard` | Dashboard metrics and actions |
| GET, POST, PATCH | `/api/tasks` | Manage study tasks |
| GET, POST | `/api/subjects` | Manage subjects |
| GET, POST | `/api/diary` | Manage reflections |
| GET, POST | `/api/notes` | List or create notes |
| GET, POST | `/api/syllabus` | List or create syllabus units |
| GET, POST | `/api/pyq` | List or create previous-year questions |
| GET, POST | `/api/timetable` | List or create timetable entries |
| GET | `/api/health` | Health check |

## Testing

From the repository root:

```powershell
python -m unittest discover -s 08_testing
```

## Production Notes

Set a long unique `JWT_SECRET_KEY`, restrict `CORS_ORIGINS`, move to PostgreSQL/object storage, add upload scanning, and complete privacy/security review before a public release.
