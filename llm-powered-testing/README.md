## Phase 1: Simulate "No RAG"

The goal is to make the model answer **only from its general knowledge** and prevent it from using the simulated internal rules.

### Prompt A — No RAG

```markdown
# Role

You are an experienced API documentation specialist and software tester.

# Task

Explain the required data structure and compliance rules for a refund transaction on a new payment processing API.

# Context / Data

No internal company documentation or proprietary compliance specification is available.
You must rely only on your general knowledge of payment processing APIs and common industry practices.

# Constraints

- Do not invent or assume company-specific rules.
- Clearly distinguish between generally accepted API practices and requirements that would need confirmation from the company.
- Do not assume that the refund identifier is named `transaction_UUID`.
- Do not assume that the API requires a 48-hour waiting period.
- If an exact requirement cannot be determined from the available information, explicitly state that it requires confirmation from the internal specification.

# Output Format

Provide:

1. Expected refund data structure
2. Common fields and their purposes
3. General compliance considerations
4. Requirements that cannot be determined without the company's internal specification

# Goal

Produce accurate, professional API documentation while making it clear which requirements are based on general knowledge rather than proprietary company rules.
```

### Expected Result

The model **should not know** the two simulated internal requirements:

- `transaction_UUID` must be used as the refund identifier.
- A **48-hour waiting period** is required before processing a refund.

Instead, it will likely provide a generic refund structure and state that the exact identifier and waiting period need to be confirmed from the company's documentation.

---

# Phase 2: Simulate "With RAG"

Here, the internal specification is retrieved by the RAG system and injected into the prompt's **Context/Data** component.

### Prompt B — With RAG

```markdown
# Role

You are an experienced API documentation specialist and software tester.

# Task

Explain the required data structure and compliance rules for a refund transaction on a new payment processing API.

# Context / Data

The following information was retrieved from the company's internal specification document:

Internal Payment API Specification:

Rule 1 — Data Structure:
The API requires the unique identifier for a refund to be named `transaction_UUID`, not `refund_ID`.

Rule 2 — Compliance:
The system mandates a 48-hour waiting period before any refund can be processed.

Use these retrieved internal rules as authoritative requirements for this API.

# Constraints

- Follow the internal specification exactly.
- Use `transaction_UUID` as the refund identifier.
- Do not use `refund_ID` as the identifier.
- State that a 48-hour waiting period is mandatory before processing a refund.
- Do not replace the company's internal requirements with generic payment API conventions.
- Clearly distinguish the company's specific requirements from any optional/general API practices.

# Output Format

Provide:

1. Required refund data structure
2. Explanation of each required field
3. Compliance rules
4. Example refund request
5. Important implementation notes

# Goal

Produce accurate API documentation based on the retrieved internal company specification.
```

### Expected Result

With the retrieved context, the model should document the company-specific requirements, for example:

```json
{
  "transaction_UUID": "550e8400-e29b-41d4-a716-446655440000",
  "amount": 100.0,
  "currency": "USD",
  "reason": "Customer requested refund"
}
```

And the documentation should explicitly state:

- The refund's unique identifier **must be named `transaction_UUID`**.
- `refund_ID` should **not** be used.
- A refund **cannot be processed until 48 hours have elapsed**.
- These requirements come from the company's internal specification.

## Comparison

| Aspect                              | No RAG — Prompt A               | With RAG — Prompt B                     |
| ----------------------------------- | ------------------------------- | --------------------------------------- |
| Internal document                   | Not available                   | Retrieved and injected                  |
| `transaction_UUID` rule             | Unknown to model                | Explicitly provided                     |
| `refund_ID` restriction             | Unknown                         | Explicitly provided                     |
| 48-hour waiting period              | Unknown                         | Explicitly provided                     |
| Knowledge source                    | General/pre-trained knowledge   | General knowledge + internal context    |
| Expected accuracy for company rules | Limited                         | High                                    |
| Main RAG benefit                    | Cannot access proprietary rules | Grounds the answer in proprietary rules |

**Key takeaway:** RAG allows the LLM to incorporate information that was not part of its general training knowledge. In this scenario, the retrieved internal specification supplies the exact `transaction_UUID` naming convention and 48-hour compliance requirement, allowing the model to produce documentation specific to the company's API.
