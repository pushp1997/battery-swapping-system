from django.test import TestCase, Client
from django.urls import reverse

# from kiosk.models import Users


class TestViews(TestCase):
    def test_kiosk_index(self):
        client = Client()
        response = client.get(reverse("kiosk_index"))
        self.assertTemplateUsed(response, "kiosk/index.html")

    def test_user_login(self):
        client = Client()
        response = client.get(reverse("user_login"))
        self.assertTemplateUsed(response, "kiosk/user-login.html")
