"""Throttle classes to limit anonymous feedback submissions."""

from typing import Any, Optional

from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import SAFE_METHODS
from rest_framework.throttling import SimpleRateThrottle


class EventFeedbackRateThrottle(SimpleRateThrottle):
    """Limit feedback submissions per client token and event."""

    scope = "feedback_event_token"
    throttle_failure_detail = _("Rate limit exceeded for this event and client token.")

    def get_cache_key(self, request: Any, view: Any) -> Optional[str]:
        if request.method in SAFE_METHODS:
            return None

        token = None
        event_id = None

        if hasattr(request, "data") and request.data:
            token = request.data.get("client_token")
            event_id = request.data.get("event") or request.data.get("event_id")

        if not token and hasattr(request, "feedback_client_token"):
            token = getattr(request, "feedback_client_token")

        if not event_id and hasattr(request, "feedback_event_id"):
            event_id = getattr(request, "feedback_event_id")

        if not token or not event_id:
            return None

        ident = f"{event_id}:{token}"
        return self.cache_format % {"scope": self.scope, "ident": ident}
