from django.test import SimpleTestCase
from django.urls import reverse, resolve
from rack.views import index


class TestUrls(SimpleTestCase):
    def test_rack_index_url_is_resolved(self):
        url = reverse("rack_index")
        self.assertEquals(resolve(url).func, index)
