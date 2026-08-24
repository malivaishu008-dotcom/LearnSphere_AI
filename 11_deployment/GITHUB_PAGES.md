# GitHub Pages Hosting Guide

GitHub Pages can host the static landing page for project presentation. The authenticated dashboard requires the Flask backend, so Pages should be treated as a public project website, not the complete production application.

## Option 1 - Publish the Existing Frontend

1. Push the repository to GitHub.
2. Open repository Settings.
3. Go to Pages.
4. Select GitHub Actions as the source.
5. Enable the `Publish static landing page` workflow included in this repository.

## What Works on Pages

- Landing page content.
- Branding and footer links.
- Project presentation.

## What Needs Backend Hosting

- Register and login.
- Dashboard data.
- Tasks, notes, syllabus, PYQ, timetable, quizzes, uploads, diary, and insights.

## Recommended Deployment Pair

- GitHub Pages: public landing/project site.
- Render/AWS/backend host: Flask API and full application.

After backend deployment, update frontend API configuration if the frontend is separated from the Flask server. In the current local MVP, the Flask app serves both frontend and API from the same origin.
