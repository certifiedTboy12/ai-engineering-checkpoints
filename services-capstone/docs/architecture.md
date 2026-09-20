# Architecture

## System Overview

```text
                    ┌──────────────────────┐
                    │      Customer        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ React Web Application │
                    │ JSX + Tailwind       │
                    │ Wouter + Motion      │
                    └──────────┬───────────┘
                               │ HTTPS / REST
                               ▼
                    ┌──────────────────────┐
                    │    Express API       │
                    │ Auth + Validation    │
                    │ Service Logic        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      MongoDB         │
                    │ Users / Services /   │
                    │ Requests / Status    │
                    └──────────────────────┘

        ┌──────────────────────────────────────────┐
        │ Supporting infrastructure                │
        │ Jest + Supertest | Docker | CI/CD       │
        └──────────────────────────────────────────┘
```

## Main Components

### Frontend

The React application presents service categories, service details, forms, dashboard information, statuses, recurring plans, and upcoming visits.

Tailwind CSS provides the visual system and responsive layouts. Wouter handles lightweight client-side routing, while Framer Motion provides interaction feedback.

### API

The Express backend exposes REST endpoints for authentication and service-management operations. Validation is applied before data is stored or processed.

### Database

MongoDB stores application data such as users, service requests, schedules, and service statuses.

### Testing

Jest and Supertest are used for automated backend/API testing. The final release should also include manual smoke testing of the critical customer journey.

## Important User Flow: Requesting a Service

### Step 1 — Customer selects a service

The customer opens the service catalogue and selects a service such as home cleaning.

### Step 2 — Customer provides details

The customer describes what needs to be done and provides the required scheduling information.

### Step 3 — Frontend validates input

The frontend checks required fields and scheduling rules before sending the request.

### Step 4 — Request is sent to the API

The React application sends an authenticated REST request to the Express backend.

```text
React Form
   ↓
Validation
   ↓
POST /api/services
   ↓
Express Controller
```

### Step 5 — Backend validates and stores data

The backend validates the request, applies business rules, and stores the service request in MongoDB.

```text
Express
   ↓
Validation / Business Rules
   ↓
MongoDB
```

### Step 6 — API returns the result

The API returns the created request and its initial status.

```json
{
  "status": "new"
}
```

### Step 7 — UI updates

The customer sees the new request and can follow its progress. Staff can see the request from the service-management dashboard.

## Design Considerations

- Keep UI components reusable.
- Keep API responsibilities separate from presentation.
- Validate data at both frontend and backend boundaries.
- Keep secrets in environment variables.
- Use explicit service statuses instead of relying on ambiguous UI text.
- Make the critical customer journey testable from request to completion.
