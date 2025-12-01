import graphene
from graphene_django import DjangoObjectType

from events.models import Event, EventType
from speakers.models import Speaker


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


class Query(graphene.ObjectType):
    all_event_types = graphene.List(EventTypeNode)
    all_events = graphene.List(EventNode)
    all_speakers = graphene.List(SpeakerNode)

    def resolve_all_event_types(self, info, **kwargs):
        return EventType.objects.all()

    def resolve_all_events(self, info, **kwargs):
        return Event.objects.select_related("event_type", "presenter").all()

    def resolve_all_speakers(self, info, **kwargs):
        return Speaker.objects.all()


schema = graphene.Schema(query=Query)
