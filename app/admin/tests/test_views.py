from django.test import TestCase, Client
from django.urls import reverse

# from kiosk.models import Users


class TestViews(TestCase):
    def test_admin_dashboard(self):
        client = Client()
        response = client.get(reverse("admin_dashboard"))
        self.assertTemplateUsed(response, "admin/admin_dashboard.html")
