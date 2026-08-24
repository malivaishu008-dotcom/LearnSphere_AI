# Three-Person Delivery Plan

| Owner | Ownership | First sprint deliverables |
| --- | --- | --- |
| Member 1 — Product & frontend | Research, UX, brand system, landing/workspace interaction, accessibility | User flows, UI acceptance checks, demo narrative |
| Member 2 — Platform & data | API, authentication, database, uploads, deployment, security | API contract, migrations, Docker/hosting, test automation |
| Member 3 — AIML & evaluation | Quiz/RAG pipeline, insight modelling, datasets, evaluation, AI safety | Evaluation set, provider adapter, bias/accuracy report |

## Operating cadence

- Monday: 30-minute scope and risks review.
- Daily: one small pull request per coherent concern; every PR has a screenshot or API example and test result.
- Thursday: integration demo using a scrubbed student journey.
- Friday: changelog, research log, risk register, and retro.

## Git workflow

Protect `main`. Use `feature/frontend-*`, `feature/platform-*`, and `feature/aiml-*` branches. Require one peer review, passing tests, no secrets, and a clear rollback note before merge. Tag demonstration releases as `v0.x.0`.
