# API Endpoints

This document describes the REST API and includes example payloads. Two main areas are covered: Admin API (`/api/admin/`) and Application API (`/api/v1/`). All examples assume `application/json` payloads.

## Obtaining JWT tokens
- `POST /api/token/` – accepts `username` and `password`; returns an `access`/`refresh` pair.
- `POST /api/token/refresh/` – accepts `refresh`; returns a new `access`.
- Send the token with `Authorization: Bearer <access_token>`.

## Admin API (`/api/admin/`)
All endpoints below require JWT authentication and an admin user (`IsAdminUser`). Views use the global `filter_backends` (filter, search, ordering) plus per-view field lists.

### Event types (`/event-types/`)
- Methods: `GET` list/detail, `POST`, `PUT/PATCH`, `DELETE`.
- Serializer: `EventTypeSerializer` – fields `id`, `name`, `description`.
- Search: `name`.
- Example `POST`:
  ```json
  {"name": "Workshop", "description": "Hands-on labs"}
  ```
- Example response:
  ```json
  {"id": 3, "name": "Workshop", "description": "Hands-on labs"}
  ```

### Events (`/events/`)
- Methods: full CRUD.
- Serializer: `EventSerializer` – fields `id`, `title`, `event_type`, `event_type_id`, `start_time`, `room`, `presenter`, `presenter_id`, `description` (relations `event_type`/`presenter` are nested on read, `*_id` are used when writing).
- Filters: `event_type`, `presenter`, `room`; search: `title`, `description`, `room`; ordering: `start_time`, `title`.
- Example `POST`:
  ```json
  {
    "title": "Keynote",
    "event_type_id": 1,
    "start_time": "2024-09-10T09:00:00Z",
    "room": "Main Hall",
    "presenter_id": 2,
    "description": "Conference opening"
  }
  ```
- Example response (abridged):
  ```json
  {
    "id": 12,
    "title": "Keynote",
    "event_type": {"id": 1, "name": "Talk", "description": "Presentation"},
    "start_time": "2024-09-10T09:00:00Z",
    "room": "Main Hall",
    "presenter": {"id": 2, "name": "Dr. Jane"},
    "description": "Conference opening"
  }
  ```

### Feedback (`/feedback/`)
- Methods: full CRUD (moderate and delete entries).
- Serializer: `FeedbackAdminSerializer` – fields `id`, `event`, `event_id`, `rating`, `comment`, `client_token`, `created_at`.
- Filters: `event`, `rating`; search: `comment`, `client_token`; ordering: `created_at`, `rating`.

### Speakers (`/speakers/`)
- Methods: full CRUD.
- Serializer: `SpeakerSerializer` – fields `id`, `name`, `bio`, `socials`, `photo`, `company`.
- Search: `name`, `company`, `bio`.

### Sponsors (`/sponsors/`)
- Methods: full CRUD.
- Serializer: `SponsorSerializer` – fields `id`, `name`, `logo_url`, `description`, `socials`.
- Search: `name`, `description`.

### Coupons (`/coupons/`)
- Methods: full CRUD.
- Serializer: `CouponSerializer` – fields `id`, `sponsor`, `sponsor_id`, `code`, `description`, `discount_amount`, `valid_from`, `valid_to`, `max_redemptions`, `is_active`, `remaining_redemptions` (read-only).
- Filters: `sponsor`; search: `code`, `description`; ordering: `valid_from`, `valid_to`, `discount_amount`, `code`.

### Coupon redemptions (`/coupon-redemptions/`)
- Methods: full CRUD (review, revert redemptions, etc.).
- Serializer: `CouponRedemptionSerializer` – fields `id`, `coupon`, `coupon_code`, `client_token`, `redeemed_at`.
- Filters: `coupon__sponsor`, `coupon`; search: `coupon__code`, `client_token`; ordering: `redeemed_at`.

## Application API (`/api/v1/`)
Publicly accessible resources (no JWT) are read-only or allow creation where appropriate. Views use `filter_backends` (filters, sorting, search) limited to the listed fields.

### Event types (`/event-types/`)
- Methods: `GET` list/detail.
- Serializer: `EventTypeSerializer` – fields `id`, `name`, `description`.
- Search: `name`.

### Events (`/events/`)
- Methods: `GET` list/detail.
- Serializer: `EventSerializer` – same fields as the admin section.
- Filters: `event_type`, `presenter`, `room`; search: `title`, `description`, `room`; ordering: `start_time`, `title`.

### Feedback (`/feedback/`)
- Methods: `GET` list/detail, `POST` create (anonymous).
- Serializer: `FeedbackSerializer` – fields `id`, `event`, `event_id`, `rating`, `comment`, `client_token`, `created_at` (`client_token` and `event_id` when writing, `event` when reading).
- Filters: `event`; ordering: `created_at`, `rating`.
- Limits: `EventFeedbackRateThrottle` (default `5/hour` per `event` + `client_token`).
- Example `POST`:
  ```json
  {"event_id": 12, "rating": 5, "comment": "Great talk!", "client_token": "device-123"}
  ```
- Example response:
  ```json
  {
    "id": 44,
    "event": {"id": 12, "title": "Keynote", "room": "Main Hall"},
    "rating": 5,
    "comment": "Great talk!",
    "created_at": "2024-09-10T10:05:00Z"
  }
  ```

### Speakers (`/speakers/`)
- Methods: `GET` list/detail.
- Serializer: `SpeakerSerializer` – fields `id`, `name`, `bio`, `socials`, `photo`, `company`.
- Search: `name`, `company`; filters: `company`.

### Sponsors (`/sponsors/`)
- Methods: `GET` list/detail.
- Serializer: `SponsorSerializer` – fields `id`, `name`, `logo_url`, `description`, `socials`.
- Search: `name`, `description`.

### Coupons (`/coupons/`)
- Methods: `GET` list/detail.
- Serializer: `CouponSerializer` – same fields as in the admin section, with `remaining_redemptions` computed in responses.
- Filters: `sponsor`, `code`; search: `code`, `description`; ordering: `valid_from`, `valid_to`, `discount_amount`, `code`.

### Coupon redemptions (`/coupon-redemptions/`)
- Methods: `POST` (anonymous redemption). No public reads.
- Serializer: `CouponRedemptionSerializer` – accepts `coupon_code`, `client_token`; returns `id`, coupon data, `redeemed_at`.
- Example `POST`:
  ```json
  {"coupon_code": "SUMMER24", "client_token": "device-123"}
  ```
- Example response:
  ```json
  {
    "id": 7,
    "coupon": {
      "id": 3,
      "code": "SUMMER24",
      "description": "20% discount",
      "discount_amount": "20.00",
      "valid_from": "2024-06-01T00:00:00Z",
      "valid_to": "2024-08-31T23:59:59Z",
      "sponsor": {"id": 2, "name": "TechCorp"},
      "remaining_redemptions": 42
    },
    "client_token": "device-123",
    "redeemed_at": "2024-06-05T12:00:00Z"
  }
  ```

## GraphQL (`/graphql/`)
GraphiQL is available in development. Example queries:
```graphql
query {
  allEvents { id title startTime room presenter { id name } }
  allSpeakers { id name company }
  allCoupons { code discountAmount sponsor { name } }
}
```
Example mutation for submitting feedback (subject to the same throttling as REST):
```graphql
mutation {
  createFeedback(eventId: 12, rating: 5, comment: "Great!", clientToken: "device-123") {
    feedback { id rating comment createdAt }
  }
}
```
