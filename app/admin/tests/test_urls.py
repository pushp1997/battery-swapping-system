from django.test import SimpleTestCase
from django.urls import reverse, resolve
from admin.views import admin_login, admin_dashboard


class TestUrls(SimpleTestCase):
    def test_admin_login_url_is_resolved(self):
        url = reverse("admin_login")
        self.assertEquals(resolve(url).func, admin_login)

    def test_admin_dashboard_url_is_resolved(self):
        url = reverse("admin_dashboard")
        self.assertEquals(resolve(url).func, admin_dashboard)
