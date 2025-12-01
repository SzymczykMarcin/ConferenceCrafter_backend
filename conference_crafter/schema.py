"""GraphQL schema exposing conference data for frontend queries."""

import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from events.models import Event, EventType, Feedback
from speakers.models import Speaker
from sponsors.models import Coupon, Sponsor


class EventTypeNode(DjangoObjectType):
    """GraphQL node for event categories including names and descriptions."""

    class Meta:
        model = EventType
        fields = ("id", "name", "description")


class SpeakerNode(DjangoObjectType):
    """GraphQL node exposing speaker biographies and company details."""

    class Meta:
        model = Speaker
        fields = ("id", "name", "bio", "socials", "photo", "company")


class EventNode(DjangoObjectType):
    """GraphQL node representing scheduled events and presenters."""

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "event_type",
            "start_time",
            "room",
            "presenter",
            "description",
        )


class FeedbackNode(DjangoObjectType):
    """GraphQL node exposing feedback details without client tokens."""

    class Meta:
        model = Feedback
        fields = ("id", "event", "rating", "comment", "created_at")


class SponsorNode(DjangoObjectType):
    """GraphQL node summarizing sponsors for marketing or scheduling."""

    class Meta:
        model = Sponsor
        fields = ("id", "name", "logo_url", "description", "socials")


class CouponNode(DjangoObjectType):
    """GraphQL node for discount codes tied to sponsors."""

    class Meta:
        model = Coupon
        fields = (
            "id",
            "code",
            "description",
            "discount_amount",
            "valid_from",
            "valid_to",
            "sponsor",
        )


class Query(graphene.ObjectType):
    """Top-level queries for browsing events, speakers, sponsors, and coupons."""

    all_event_types = graphene.List(
        EventTypeNode, description="Retrieve every event category available for scheduling."
    )
    all_events = graphene.List(
        EventNode, description="List all scheduled events with presenter and type details."
    )
    all_speakers = graphene.List(
        SpeakerNode, description="List all speakers with biographies and contact details."
    )
    all_sponsors = graphene.List(
        SponsorNode, description="List all sponsors supporting the conference."
    )
    all_coupons = graphene.List(
        CouponNode, description="List sponsor coupons along with validity windows."
    )
    all_feedback = graphene.List(
        FeedbackNode,
        event_id=graphene.ID(required=False),
        description="List public feedback, optionally filtered by event.",
    )

    def resolve_all_event_types(self, info, **kwargs):
        """Return all event types sorted per model defaults."""

        return EventType.objects.all()

    def resolve_all_events(self, info, **kwargs):
        """Return all events with related event types and presenters prefetched."""

        return Event.objects.select_related("event_type", "presenter").all()

    def resolve_all_speakers(self, info, **kwargs):
        """Return all speaker profiles."""

        return Speaker.objects.all()

    def resolve_all_sponsors(self, info, **kwargs):
        """Return all sponsors available to frontend clients."""

        return Sponsor.objects.all()

    def resolve_all_coupons(self, info, **kwargs):
        """Return all coupons with sponsor relationships loaded."""

        return Coupon.objects.select_related("sponsor").all()

    def resolve_all_feedback(self, info, event_id=None, **kwargs):
        """Return feedback entries, optionally scoped to a single event."""

        queryset = Feedback.objects.select_related("event").all()
        if event_id:
            queryset = queryset.filter(event_id=event_id)
        return queryset


class CreateFeedback(graphene.Mutation):
    """Mutation for anonymous feedback submission with throttling protection."""

    feedback = graphene.Field(FeedbackNode)

    class Arguments:
        event_id = graphene.ID(required=True)
        rating = graphene.Int(required=True)
        comment = graphene.String(required=False)
        client_token = graphene.String(required=True)

    @staticmethod
    def mutate(root, info, event_id, rating, client_token, comment=None):
        from events.throttling import EventFeedbackRateThrottle

        request = info.context
        request.feedback_event_id = event_id
        request.feedback_client_token = client_token

        throttle = EventFeedbackRateThrottle()
        if not throttle.allow_request(request, info):
            raise GraphQLError(str(throttle.throttle_failure_detail))

        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist as exc:  # pragma: no cover - guarded by DB
            raise GraphQLError("Event not found.") from exc

        if rating < 1 or rating > 5:
            raise GraphQLError("Rating must be between 1 and 5.")

        feedback = Feedback.objects.create(
            event=event,
            rating=rating,
            comment=comment or "",
            client_token=client_token,
        )

        return CreateFeedback(feedback=feedback)


class Mutation(graphene.ObjectType):
    create_feedback = CreateFeedback.Field(description="Submit anonymous feedback for an event.")


schema = graphene.Schema(query=Query, mutation=Mutation)
