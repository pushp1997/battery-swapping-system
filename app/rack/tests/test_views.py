from django.test import TestCase, Client
from django.urls import reverse

# from kiosk.models import Users


class TestViews(TestCase):
    def test_rack_index(self):
        client = Client()
        response = client.get(reverse("rack_index"))
        self.assertTemplateUsed(response, "rack/index.html")
