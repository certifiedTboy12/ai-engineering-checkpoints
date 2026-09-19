# FastAPI Claude Code Checkpoint

## Project Overview

This is a small FastAPI project used to demonstrate a safe and reviewable Claude Code workflow.

The application currently provides:

- `GET /`
- `GET /health`

Tests are written with pytest and FastAPI TestClient.

## Folder Structure

```text
app/
    main.py              # FastAPI application

tests/
    test_main.py         # API tests

docs/
    claude-code-checkpoint.md
    claude-rules.md

.claude/
    commands/            # Project slash commands
    memory.md            # Stable project facts
    settings.local.json  # Local Claude Code permissions