# Syncflow Backend Overview

This document provides an overview of the backend structure and the main API endpoints available in the Syncflow backend.

## Backend Structure

- `apps/`: Contains Django apps that implement various features of the platform.
  - `UserAccount`: Handles user authentication, registration, profile management, and email verification.
  - `social`: Manages social media authentication and integration.
  - `analytics`: Provides analytics-related functionality.
  - `automations`: Contains AI automation features including models, agents, and tasks.
  - `campaigns`: Manages marketing campaigns.
  - `core`: Core business logic and shared functionality.
  - `integrations`: External service integrations.
- `syncflow/`: Main Django project configuration including settings, URLs, ASGI/WSGI, and Celery.
- `tasks/`: Background task definitions.
- `static/` and `templates/`: Static assets and HTML templates.

## Main API Endpoints

The backend exposes REST API endpoints under the `/api/` path, organized by app:

### User Account (`/api/accounts/`)

Handles user authentication, registration, profile management, password reset, and email verification.

- `auth/register/`: User registration endpoint allowing new users to create accounts.
- `auth/login/`: User login endpoint for obtaining authentication tokens.
- `auth/logout/`: User logout endpoint to invalidate tokens.
- `auth/user/`: Retrieves details of the currently authenticated user.
- `auth/password/reset/`: Initiates password reset process by sending reset email.
- `auth/password/reset/confirm/<uidb64>/<token>/`: Confirms password reset with token.
- `auth/password/change/`: Allows authenticated users to change their password.
- `auth/verify-email/`: Endpoint to verify user email addresses.
- `account-confirm-email/<str:key>/`: Confirms email verification via key.
- `account-email-verification-sent/`: Notification endpoint for email verification sent.
- `profile/`: User profile management including viewing and updating profile data.

### Social (`/api/social/`)

Manages social media authentication and integration.

- `auth/<platform>/init/`: Initializes social authentication flow for specified platform (e.g., Facebook, Google).
- `auth/callback/`: Callback endpoint to handle social authentication responses.

### Analytics (`/api/analytics/`)

Currently no API endpoints are defined. This app is intended to provide analytics data and reports related to platform usage and social media performance.

### Automations (`/api/automations/`)

Provides AI automation features including management of large language model (LLM) providers, AI models, AI agents, and agent tasks.

- `llm-providers/`: CRUD operations for LLM providers.
- `ai-models/`: CRUD operations for AI models linked to providers.
- `ai-agents/`: CRUD operations for AI agents that perform specific tasks.
- `agent-tasks/`: Read-only access to tasks executed by AI agents.

The app supports asynchronous execution of agent tasks and integration with external AI services.

### Campaigns (`/api/campaigns/`)

Currently no API endpoints are defined. This app is designed to manage marketing campaigns, including creation, scheduling, and tracking.

### Core (`/api/`)

Contains core business logic and shared functionality.

- `brands/`: List and create brand entities.
- `brands/<int:pk>/`: Retrieve, update, or delete specific brand details.

### Integrations (`/api/integrations/`)

Currently no API endpoints are defined. This app is intended for managing external service integrations.

### API Documentation

- `/api/schema/`: OpenAPI schema endpoint for API specification.
- `/api/docs/`: Swagger UI for interactive API documentation.
- `/api/redoc/`: ReDoc UI for API documentation.

### Admin

- `/admin/`: Django admin interface for managing backend data and configurations.

## Additional Notes

- Authentication is primarily handled via JWT tokens with cookies.
- Social authentication uses `django-allauth` and supports Google, Facebook, and Apple.
- Background tasks are managed with Celery.
- Static files are served using WhiteNoise.

For detailed endpoint information, refer to the respective app's `urls.py` and view implementations.

## App Descriptions and Flows

### UserAccount

This app manages user authentication and account management. It supports registration, login, logout, password reset and change, email verification, and user profile management. The flow typically involves user registration, email verification, login to obtain JWT tokens, and profile updates. Password reset and change flows are also supported.

### Social

Handles social media authentication via OAuth for platforms like Facebook and Google. The flow involves initializing social login, redirecting users to the provider, and handling callback responses to authenticate users.

### Analytics

Currently provides analytics-related functionality, though no public API endpoints are defined. It is intended to collect and report data on platform usage and social media performance.

### Automations

This app provides AI automation capabilities. It manages large language model providers, AI models, AI agents that perform tasks, and agent tasks themselves. The flow includes creating and managing AI models and agents, submitting tasks for execution, and retrieving task results. It integrates with external AI services asynchronously.

### Campaigns

Designed to manage marketing campaigns including creation, scheduling, and tracking. Currently, no API endpoints are defined.

### Core

Contains core business logic and shared functionality. It includes management of brand entities with endpoints to list, create, update, and delete brands.

### Integrations


## Additional Notes

- Authentication is primarily handled via JWT tokens with cookies.
- Social authentication uses `django-allauth` and supports Google, Facebook, and Apple.
- Background tasks are managed with Celery.
- Static files are served using WhiteNoise.

For detailed endpoint information, refer to the respective app's `urls.py` and view implementations.
