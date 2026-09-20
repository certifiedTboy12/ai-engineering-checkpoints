# Home Services Management Platform

A full-stack service management platform for requesting, scheduling, tracking, and managing home services such as cleaning and pest control.

## Problem

Home-service customers often have to coordinate requests, schedules, service details, communication, and completion evidence across disconnected channels. Service providers also need a consistent way to manage requests and service status.

## Solution

This project provides a centralized web application where customers can request services and track their service journey while service teams can manage requests, schedules, statuses, and completion information from a dashboard.

## Features

- Customer service-request workflow
- Service categories and service cards
- Service details and enquiry prompts
- Scheduling and service-date validation
- Upcoming/next-service view
- Recurring-service plan support
- Service status tracking: new, active, pending, completed, cancelled
- Dashboard for service management
- Customer/service communication area
- Completion evidence and checklist concepts
- Responsive UI for desktop and mobile
- Authentication-ready application structure
- API-based backend integration
- Validation and error handling

## Tech Stack

### Frontend
- React
- JSX
- Tailwind CSS
- Wouter
- Framer Motion
- Lucide React

### Backend / Data
- Node.js
- Express.js
- MongoDB
- REST APIs

### Quality / DevOps
- Jest
- Supertest
- Docker
- GitHub Actions / CI
- Vercel or another frontend deployment platform

> Update the deployment provider and repository links below with the final live values before submission.

## Project Structure

```text
.
├── src/
├── public/
├── docs/
│   ├── architecture.md
│   ├── final-product-review.md
│   ├── final-release-checklist.md
│   └── portfolio-case-study.md
├── README.md
├── Dockerfile
├── docker-compose.yml
├── package.json
└── .env.example
```

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_NAME>
```

### 2. Install dependencies

```bash
npm install
```

If the backend is a separate application:

```bash
cd backend
npm install
```

### 3. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Add the required values locally. Never commit the real `.env` file.

### 4. Start the application

```bash
npm run dev
```

For a separate backend:

```bash
npm run server
```

Use the project's existing scripts if they differ from these examples.

## Environment Variables

Example variables:

```env
PORT=3000
MONGODB_URI=mongodb://localhost:27017/home-services
JWT_SECRET=replace-with-a-long-random-secret
CLIENT_URL=http://localhost:5173
```

Do not place production credentials, API keys, JWT secrets, database passwords, OAuth secrets, or private tokens in Git.

## Testing

Run the test suite with:

```bash
npm test
```

For API tests using Jest and Supertest:

```bash
npm test -- --runInBand
```

Add the exact command used by the final repository if the package scripts use different names.

## API Example

Example service request:

```http
POST /api/services
Content-Type: application/json
Authorization: Bearer <ACCESS_TOKEN>
```

```json
{
  "service": "home-clean",
  "description": "Deep cleaning for a two-bedroom apartment",
  "scheduledDate": "2026-10-04"
}
```

Example response:

```json
{
  "id": "service-request-id",
  "status": "new",
  "service": "home-clean",
  "scheduledDate": "2026-10-04"
}
```

## Screenshots

Add final screenshots before submission:

```text
docs/screenshots/
├── home.png
├── service-request.png
├── dashboard.png
└── next-service.png
```

Then reference them from this README, for example:

```markdown
![Dashboard](docs/screenshots/dashboard.png)
```

## Documentation

- [Final Product Review](docs/final-product-review.md)
- [Release Checklist](docs/final-release-checklist.md)
- [Architecture](docs/architecture.md)
- [Portfolio Case Study](docs/portfolio-case-study.md)

## Links

- Repository: `<YOUR_GITHUB_REPOSITORY_URL>`
- Live Demo: `<YOUR_LIVE_DEMO_URL>`
- API: `<YOUR_API_URL>`
- Portfolio: `<YOUR_PORTFOLIO_URL>`
- LinkedIn: `<YOUR_LINKEDIN_URL>`

## Security

- Real secrets are excluded from Git.
- `.env` is ignored and `.env.example` contains placeholders only.
- Authentication credentials are not hard-coded.
- Input validation is applied to service requests.
- Protected API routes require authentication where applicable.
- Production secrets should be managed by the deployment platform.

## Status

Capstone release candidate. Complete the release checklist and replace all placeholder links before final presentation.
