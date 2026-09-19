# Test Rules

Tests in this directory must follow these rules:

1. Use pytest.
2. Use FastAPI TestClient for API endpoint tests.
3. Every new endpoint should have at least one relevant test.
4. Tests should verify both HTTP status and important response data.
5. Do not disable or weaken existing tests just to make them pass.
6. Do not use real credentials, external production services, or real user data.
7. Keep tests deterministic and independent.
8. Run `pytest -q` after test changes.
