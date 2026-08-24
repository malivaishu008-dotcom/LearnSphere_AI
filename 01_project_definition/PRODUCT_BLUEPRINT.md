# LearnSphere AI — Product Blueprint

## Abstract

LearnSphere AI is a student-centred study operating system. It transforms scattered academic material and vague intentions into a daily loop: capture learning resources, plan focused work, practise recall, reflect, and adapt. It is designed as an AIML-enabled learning companion—not an automated authority on grades or academic decisions.

## Product thesis

Students commonly own content but lack a reliable operating rhythm. LearnSphere brings their subjects, notes, books, PDFs, plans, practice and reflection into a single private workspace. Its intelligence should make a next action clearer, not make the product noisier.

## Primary users and jobs

| User | Core job | Product response |
| --- | --- | --- |
| College student | Prepare consistently across several subjects | Planner, focus logging, resource library, recall practice |
| Exam candidate | Identify gaps and build confidence | Topic quizzes, sample-paper plan, revision signals |
| Reflective learner | Understand why momentum changes | Diary, consistency trends, next-action recommendations |

## Experience architecture

```text
Landing → Account → Overview
                    ├─ Study planner (subjects, tasks, timetable)
                    ├─ Knowledge base (notes, PDFs/books, voice notes)
                    ├─ Practice lab (MCQ, surprise tests, sample papers, mind maps)
                    ├─ Learning insights (consistency and scenario modelling)
                    ├─ Daily diary (reflection and habit signals)
                    └─ AI connections (approved provider routes)
```

## Delivery status

The MVP implements account access, persistent student data, study planning, document/voice-file upload, notes, diary, focus sessions, simple practice quizzes, local study-coach fallback, and indicative learning insights. Mind maps, document extraction/RAG, notifications, real scheduling, sample-paper generation, real voice transcription, provider OAuth, and production ML are intentionally staged for later delivery.

## Technology blueprint

- **Web:** responsive SPA using semantic HTML, modern CSS, and modular browser JavaScript.
- **API:** Flask REST API with JWT access control and input validation.
- **Data:** SQLite for local MVP; PostgreSQL for production.
- **Files:** local protected upload directory for MVP; private object storage in production.
- **AI:** provider adapter on the server; document-grounded Responses API route after evaluation and consent.
- **Operations:** Docker + Gunicorn, environment-based secrets, CI tests, structured logging, and error monitoring.

## AI and privacy guardrails

1. Never collect a student’s external-provider password. Use server-held project API credentials or OAuth.
2. Explain before sending any uploaded material to an AI provider; default to no external processing.
3. Treat performance predictions as indicative study signals, with a confidence label and explanation.
4. Permit export/deletion of student data before public release.
5. Evaluate generated quiz content for accuracy, age appropriateness, bias, and citation quality.

## Success measures

- Weekly active learners and week-2 retention.
- Planned vs logged focus minutes, without rewarding unhealthy overwork.
- Quiz completion and error-to-revision conversion.
- Time to first useful study plan after registration.
- Student-reported clarity and trust.
