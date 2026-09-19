# Fix Tests

Run the project's test suite.

If tests fail:

1. Read the relevant failure.
2. Inspect only the necessary files.
3. Determine the likely cause.
4. Propose the smallest fix.
5. Explain the proposed change before editing.

Do not weaken, remove, or skip tests simply to make the test suite pass.

After an approved fix, run:

```bash
pytest -q
```
