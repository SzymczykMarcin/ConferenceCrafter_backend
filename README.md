# Conference Crafter Backend

Django backend for managing conference events and speakers with admin CRUD APIs and public, Flutter-friendly endpoints.

## Prerequisites
- Python 3.11+
- Virtual environment tooling (`python -m venv venv`)

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Apply migrations:
   ```bash
   python manage.py migrate
   ```
3. Create an admin user for managing events/speakers:
   ```bash
   python manage.py createsuperuser
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Authentication & Permissions
- Admin CRUD endpoints require an authenticated admin (staff) user.
- JWT authentication is provided via:
  - `POST /api/token/` to obtain an access/refresh token pair.
  - `POST /api/token/refresh/` to refresh an access token.
- Public read-only endpoints allow unauthenticated access for event and speaker listings (suitable for Flutter clients).

## REST API Overview
- Admin routes (CRUD):
  - `GET/POST/PUT/PATCH/DELETE /api/admin/event-types/`
  - `GET/POST/PUT/PATCH/DELETE /api/admin/events/`
  - `GET/POST/PUT/PATCH/DELETE /api/admin/speakers/`
- Public routes (read-only):
  - `GET /api/v1/event-types/`
  - `GET /api/v1/events/`
  - `GET /api/v1/speakers/`

Filtering and searching are enabled for common fields (event type, presenter, room, company, text search).

## GraphQL API
- Endpoint: `POST /graphql/` (GraphiQL enabled in development)
- Queries:
  - `allEventTypes { id name description }`
  - `allEvents { id title eventType { id name } startTime room presenter { id name } description }`
  - `allSpeakers { id name bio company socials photo }`

## Running Checks
- Run Django system checks and tests:
  ```bash
  python manage.py check
  python manage.py test
  ```

## Project Structure
- `conference_crafter/` – project configuration, settings, URL routing, GraphQL schema.
- `events/` – event type and event models, admin configuration, serializers, and viewsets.
- `speakers/` – speaker models, admin configuration, serializers, and viewsets.

## Database
SQLite is used by default for development. Configure alternative databases via the `DATABASES` setting or environment variables.
