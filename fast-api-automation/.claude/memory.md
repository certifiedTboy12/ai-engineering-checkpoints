# Project Memory

## Stable Project Facts

- The project is a small FastAPI application.
- The main application entry point is `app/main.py`.
- Tests are located under `tests/`.
- pytest is used for testing.
- The standard test command is `pytest -q`.
- The application is normally started with `uvicorn app.main:app --reload`.
- API tests use FastAPI TestClient.
- The project follows small, focused changes.

## Security

- Secrets must never be stored in this file.
- Environment variables must not be copied into project memory.
- Temporary guesses and task-specific assumptions should not be stored here.
