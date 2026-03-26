# DotFlow Agent Instructions

## Project overview
DotFlow is a local-first content scheduling and push platform for Dot. e-ink devices.

## Working style
- Work only in the local repository.
- Do not create git commits.
- Do not create branches.
- Do not open pull requests.
- Modify files directly in the working tree.
- Before making large changes, explain the plan briefly.
- Prefer incremental changes over large rewrites.
- Keep the project easy to run locally with Docker.

## Tech stack
- Backend: Python
- API framework: FastAPI
- Scheduler: APScheduler
- Storage: SQLite
- Frontend: React + Vite
- Deployment: Docker Compose

## Architecture rules
- Keep Dot API integration isolated in a dedicated client module.
- Keep service plugins isolated behind a common interface.
- Keep scheduler logic separate from API routes.
- Keep API response format consistent.
- Use environment variables for secrets and tokens.
- Do not hardcode API keys.

## Code quality rules
- Prefer clear and maintainable code over clever code.
- Add basic error handling and logging.
- Avoid unnecessary abstractions.
- Add docstrings or comments only where they improve clarity.
- Preserve existing file structure unless there is a strong reason to change it.

## Safety rules
- Never delete unrelated files.
- Never overwrite large sections of code without checking dependencies.
- If a task is ambiguous, make the smallest reasonable change and explain assumptions.
- If an external API detail is unclear, leave a TODO and isolate the uncertainty.

## Delivery rules
When finishing a task:
1. Summarize what changed
2. List files created or modified
3. Mention any TODOs or follow-up items
4. Do not commit anything