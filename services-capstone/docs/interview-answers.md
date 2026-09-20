# Capstone Interview Questions and Answers

## 1. Why did you choose this stack?

I chose React because the application has multiple interactive views and reusable UI components. Tailwind CSS makes it practical to maintain a consistent responsive design. Wouter provides lightweight routing, while Framer Motion improves interaction feedback.

For the backend, Node.js and Express fit naturally with a JavaScript-based frontend and are well suited to REST APIs. MongoDB is appropriate for service requests and related application data because the data model can evolve as the product grows.

## 2. How does authentication work?

The application is designed around authenticated API access. A user authenticates, receives an access credential such as a token, and protected requests include that credential. The backend validates the credential before allowing access to protected resources.

For a production release, I would verify token expiration, secure storage, authorization checks, rate limiting, and secure cookie/token configuration according to the final authentication implementation.

## 3. How is data stored?

Service requests and related records are stored in MongoDB. The backend exposes REST endpoints that validate incoming data before writing it to the database.

A typical request contains the service type, description, schedule, customer information, and status. The status can move through defined states such as new, active, pending, completed, or cancelled.

## 4. How are errors handled?

Errors are handled at multiple boundaries. The frontend validates user input before submitting requests and should show useful feedback when a request fails. The backend validates incoming data and returns appropriate HTTP responses when data is invalid or an operation cannot be completed.

Production improvements would include centralized error handling, structured logging, request IDs, and an error-monitoring service.

## 5. What would you improve next?

I would prioritize role-based access control, real-time notifications, provider assignment, online payments, photo-based completion evidence, end-to-end browser tests, and production monitoring.

These improvements would make the platform closer to a production service-management product while also improving reliability and operational visibility.
