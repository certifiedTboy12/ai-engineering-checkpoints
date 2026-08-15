# API Test Report

## 1. Health Endpoint

### Endpoint

GET /health

### Expected Result

HTTP 200

### Response

{
"status": "healthy",
"version": "1.0.0",
"timestamp": "2026-08-15T..."
}

The endpoint does not call the AI model.

---

## 2. Chat Endpoint

### Valid Request

POST /chat

{
"message": "Explain Python."
}

Expected:
HTTP 200

Response contains an `answer` field.

### Invalid Request

{
"message": ""
}

Expected:
HTTP 422

Reason:
The message must contain at least one character.

---

## 3. Quiz Endpoint

### Valid Request

POST /quiz

{
"topic": "Python",
"number_of_questions": 5
}

Expected:
HTTP 200

Response contains a `questions` list.

### Invalid Request

{
"topic": "Python",
"number_of_questions": 50
}

Expected:
HTTP 422

Reason:
The number of questions cannot exceed 20.

---

## 4. Summarise Endpoint

### Valid Request

POST /summarise

{
"text": "Python is a programming language...",
"max_bullets": 3
}

Expected:
HTTP 200

Response contains a `summary` list.

---

## 5. Automated Tests

Tests were created using pytest and FastAPI's HTTP test client.

Endpoints tested:

- GET /health
- POST /chat
- POST /chat validation

Expected result:

All tests pass successfully.
