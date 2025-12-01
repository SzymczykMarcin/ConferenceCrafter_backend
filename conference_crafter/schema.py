import graphene
from graphene_django import DjangoObjectType

from events.models import Event, EventType
from speakers.models import Speaker
from sponsors.models import Coupon, Sponsor


class EventTypeNode(DjangoObjectType):
    class Meta:
        model = EventType
        fields = ("id", "name", "description")


class SpeakerNode(DjangoObjectType):
    class Meta:
        model = Speaker
        fields = ("id", "name", "bio", "socials", "photo", "company")


class EventNode(DjangoObjectType):
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


class SponsorNode(DjangoObjectType):
    class Meta:
        model = Sponsor
        fields = ("id", "name", "logo_url", "description", "socials")


class CouponNode(DjangoObjectType):
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
    all_event_types = graphene.List(EventTypeNode)
    all_events = graphene.List(EventNode)
    all_speakers = graphene.List(SpeakerNode)
    all_sponsors = graphene.List(SponsorNode)
    all_coupons = graphene.List(CouponNode)

    def resolve_all_event_types(self, info, **kwargs):
        return EventType.objects.all()

    def resolve_all_events(self, info, **kwargs):
        return Event.objects.select_related("event_type", "presenter").all()

    def resolve_all_speakers(self, info, **kwargs):
        return Speaker.objects.all()

    def resolve_all_sponsors(self, info, **kwargs):
        return Sponsor.objects.all()

    def resolve_all_coupons(self, info, **kwargs):
        return Coupon.objects.select_related("sponsor").all()


schema = graphene.Schema(query=Query)
