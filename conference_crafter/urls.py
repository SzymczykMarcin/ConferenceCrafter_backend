"""Project-level URL configuration for REST and GraphQL access points."""

from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from events.views import EventAdminViewSet, EventTypeAdminViewSet, EventTypeViewSet, EventViewSet
from speakers.views import SpeakerAdminViewSet, SpeakerViewSet
from sponsors.views import (
    CouponAdminViewSet,
    CouponViewSet,
    SponsorAdminViewSet,
    SponsorViewSet,
)

admin_router = routers.DefaultRouter()
admin_router.register(
    r"event-types",
    EventTypeAdminViewSet,
    basename="admin-event-type",
)
admin_router.register(
    r"events",
    EventAdminViewSet,
    basename="admin-event",
)
admin_router.register(
    r"speakers",
    SpeakerAdminViewSet,
    basename="admin-speaker",
)
admin_router.register(
    r"sponsors",
    SponsorAdminViewSet,
    basename="admin-sponsor",
)
admin_router.register(
    r"coupons",
    CouponAdminViewSet,
    basename="admin-coupon",
)

user_router = routers.DefaultRouter()
user_router.register(
    r"event-types",
    EventTypeViewSet,
    basename="event-type",
)
user_router.register(
    r"events",
    EventViewSet,
    basename="event",
)
user_router.register(
    r"speakers",
    SpeakerViewSet,
    basename="speaker",
)
user_router.register(
    r"sponsors",
    SponsorViewSet,
    basename="sponsor",
)
user_router.register(
    r"coupons",
    CouponViewSet,
    basename="coupon",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/admin/", include(admin_router.urls)),
    path("api/v1/", include(user_router.urls)),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
