from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from .models import Coupon, CouponRedemption, Sponsor

User = get_user_model()


class SponsorCouponAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="admin", email="admin@example.com", password="password", is_staff=True
        )
        self.sponsor = Sponsor.objects.create(
            name="Test Sponsor", logo_url="https://example.com/logo.png", description="Great"
        )
        now = timezone.now()
        self.coupon = Coupon.objects.create(
            sponsor=self.sponsor,
            code="SAVE10",
            description="10% off",
            discount_amount=10,
            valid_from=now,
            valid_to=now + timedelta(days=10),
            max_redemptions=2,
        )

    def test_admin_can_crud_sponsor(self):
        self.client.force_authenticate(self.admin_user)
        create_response = self.client.post(
            "/api/admin/sponsors/",
            {"name": "New Sponsor", "logo_url": "https://example.com/logo2.png", "description": "Desc"},
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)
        sponsor_id = create_response.data["id"]

        update_response = self.client.patch(
            f"/api/admin/sponsors/{sponsor_id}/",
            {"description": "Updated"},
            format="json",
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data["description"], "Updated")

        delete_response = self.client.delete(f"/api/admin/sponsors/{sponsor_id}/")
        self.assertEqual(delete_response.status_code, 204)

    def test_admin_can_crud_coupon(self):
        self.client.force_authenticate(self.admin_user)
        now = timezone.now()
        create_response = self.client.post(
            "/api/admin/coupons/",
            {
                "sponsor_id": self.sponsor.id,
                "code": "NEW50",
                "description": "Half off",
                "discount_amount": 50,
                "valid_from": now,
                "valid_to": now + timedelta(days=5),
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)
        coupon_id = create_response.data["id"]

        update_response = self.client.patch(
            f"/api/admin/coupons/{coupon_id}/",
            {"discount_amount": "55.00"},
            format="json",
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data["discount_amount"], "55.00")

        delete_response = self.client.delete(f"/api/admin/coupons/{coupon_id}/")
        self.assertEqual(delete_response.status_code, 204)

    def test_public_can_read_sponsors_and_coupons(self):
        sponsor_response = self.client.get("/api/v1/sponsors/")
        self.assertEqual(sponsor_response.status_code, 200)
        self.assertGreaterEqual(len(sponsor_response.data), 1)
        self.assertEqual(sponsor_response.data[0]["name"], self.sponsor.name)

        coupon_response = self.client.get("/api/v1/coupons/")
        self.assertEqual(coupon_response.status_code, 200)
        self.assertGreaterEqual(len(coupon_response.data), 1)
        self.assertEqual(coupon_response.data[0]["code"], self.coupon.code)
        self.assertEqual(coupon_response.data[0]["sponsor"]["id"], self.sponsor.id)
        self.assertEqual(coupon_response.data[0]["remaining_redemptions"], 2)

    def test_coupon_validation_dates(self):
        self.client.force_authenticate(self.admin_user)
        now = timezone.now()
        response = self.client.post(
            "/api/admin/coupons/",
            {
                "sponsor_id": self.sponsor.id,
                "code": "BAD",
                "description": "Invalid",
                "discount_amount": 5,
                "valid_from": now + timedelta(days=1),
                "valid_to": now,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("valid_to", str(response.data))

    def test_public_can_redeem_coupon_once_per_client(self):
        response = self.client.post(
            "/api/v1/coupon-redemptions/",
            {"coupon_code": self.coupon.code, "client_token": "device-123"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CouponRedemption.objects.count(), 1)

        repeat_response = self.client.post(
            "/api/v1/coupon-redemptions/",
            {"coupon_code": self.coupon.code, "client_token": "device-123"},
            format="json",
        )
        self.assertEqual(repeat_response.status_code, 400)
        self.assertIn("already", str(repeat_response.data))

    def test_coupon_respects_max_redemptions_and_validity(self):
        self.coupon.max_redemptions = 1
        self.coupon.save()

        first = self.client.post(
            "/api/v1/coupon-redemptions/",
            {"coupon_code": self.coupon.code, "client_token": "token-1"},
            format="json",
        )
        self.assertEqual(first.status_code, 201)

        second = self.client.post(
            "/api/v1/coupon-redemptions/",
            {"coupon_code": self.coupon.code, "client_token": "token-2"},
            format="json",
        )
        self.assertEqual(second.status_code, 400)

        self.coupon.valid_from = timezone.now() + timedelta(days=1)
        self.coupon.save()
        future_attempt = self.client.post(
            "/api/v1/coupon-redemptions/",
            {"coupon_code": self.coupon.code, "client_token": "token-3"},
            format="json",
        )
        self.assertEqual(future_attempt.status_code, 400)
