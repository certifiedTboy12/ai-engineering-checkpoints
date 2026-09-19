# Claude Code Rules Summary

Claude Code identified the following project rules:

- The project is a small FastAPI application.
- `app/main.py` contains the application.
- pytest is used for tests.
- `pytest -q` is the standard test command.
- API changes should include appropriate tests.
- Changes should remain small and focused.
- Secrets must not be accessed or exposed.
- `.env` and secret directories are protected.
- Environment-printing commands are denied.
- Destructive shell commands are denied.
- Changes should be reviewed using `git diff`.
- Features should be planned and approved before implementation.
- Documentation should describe actual completed work.
