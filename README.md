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
  - `GET/POST/PUT/PATCH/DELETE /api/admin/sponsors/`
  - `GET/POST/PUT/PATCH/DELETE /api/admin/coupons/`
  - `GET/POST/PUT/PATCH/DELETE /api/admin/coupon-redemptions/`
  - `GET/POST/PUT/PATCH/DELETE /api/admin/feedback/`
- Public routes (read-only):
  - `GET /api/v1/event-types/`
  - `GET /api/v1/events/`
  - `GET /api/v1/speakers/`
  - `GET /api/v1/sponsors/`
  - `GET /api/v1/coupons/`
  - `POST /api/v1/coupon-redemptions/` (redeem a coupon by `coupon_code` and `client_token`, enforcing validity windows and optional per-code quotas; returns remaining quota when available)
  - `GET /api/v1/feedback/`
- Public create route:
  - `POST /api/v1/feedback/` (submit anonymous feedback using `event_id`, `rating`, `comment`, `client_token`)
    - Submissions are throttled per event and client token (default `5/hour`).

Filtering and searching are enabled for common fields (event type, presenter, room, company, sponsor, coupon code, text search).

## GraphQL API
- Endpoint: `POST /graphql/` (GraphiQL enabled in development)
- Queries:
  - `allEventTypes { id name description }`
  - `allEvents { id title eventType { id name } startTime room presenter { id name } description }`
  - `allSpeakers { id name bio company socials photo }`
  - `allSponsors { id name logoUrl description socials }`
  - `allCoupons { id code description discountAmount validFrom validTo sponsor { id name } }`
  - `allFeedback(eventId: ID) { id rating comment createdAt event { id title } }`
- Mutation:
  - `createFeedback(eventId: ID!, rating: Int!, comment: String, clientToken: String!) { feedback { id rating comment createdAt event { id title } } }`

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
- `sponsors/` – sponsor and coupon models, admin configuration, serializers, viewsets, and tests.
  - Coupon redemptions are recorded with an anonymous `client_token`, enforce optional `max_redemptions`, and can be managed via admin or `POST /api/v1/coupon-redemptions/`.

## Database
SQLite is used by default for development. Configure alternative databases via the `DATABASES` setting or environment variables.
