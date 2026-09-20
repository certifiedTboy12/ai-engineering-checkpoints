# 3–5 Minute Capstone Demo Script

## 0:00–0:30 — Opening

"Hello, this is my capstone project, the Home Services Management Platform.

The goal is to give customers a simple way to discover a service, submit a request, choose a schedule, and track what happens next, while giving service teams a structured way to manage those requests."

## 0:30–1:00 — Problem

"Traditional home-service requests can become fragmented across messages, phone calls, spreadsheets, and manual follow-ups.

This project brings the main workflow into one application."

## 1:00–2:15 — Main Features

1. Open the home page and show the service categories.
2. Select a service.
3. Show the service details and enquiry/request action.
4. Complete the request form.
5. Demonstrate validation and scheduling.
6. Submit the request.
7. Open the dashboard.
8. Show the service status.
9. Show the upcoming/next-service component.
10. Show the recurring-plan component if enabled.

Suggested narration:

"The interface is built around a clear service journey. The customer starts with a service, provides the required details, receives validation feedback, and then sees the request represented in the service-management workflow."

## 2:15–3:00 — Technical Architecture

"The frontend is built with React, JavaScript, Tailwind CSS, Wouter, Framer Motion, and Lucide icons.

The backend uses Node.js and Express to expose REST APIs, while MongoDB provides persistent storage.

The basic flow is React frontend to Express API to MongoDB, with validation at the application boundaries."

Show:

```text
React → REST API → Express → MongoDB
```

## 3:00–3:40 — Test / Deployment Proof

"To support quality, the project uses Jest and Supertest for API testing. The repository also includes Docker and CI/CD preparation.

I would now show the test command and the successful test result, followed by the deployed application if a production URL is available."

Run:

```bash
npm test
```

Then show the live URL.

## 3:40–4:30 — Closing

"The main lesson from this project was learning to think beyond individual components and design the complete product workflow.

I practiced frontend development, backend APIs, data persistence, validation, testing, Docker, CI/CD, and technical documentation.

The next version would add stronger role-based access control, payments, real-time notifications, provider assignment, and end-to-end testing.

Thank you."
