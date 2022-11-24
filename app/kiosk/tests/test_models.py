from django.test import TestCase
from kiosk.models import Users


class TestUsers(TestCase):
    def test_setUp(self):
        self.user1 = Users.objects.create(
            pin=1234,
            name="Test User1",
            email_id="user1@test.com",
            phone_no="+353894890221",
            driving_license="DRIVINGLICENSE1",
            allowed_batteries=3,
            user_recharge=1000,
            admin_flag=False,
        )
        self.assertIsInstance(self.user1, Users)

        self.user2 = Users.objects.create(
            pin=1234,
            name="Test User2",
            email_id="user2@test.com",
            phone_no="+353894890221",
            driving_license="DRIVINGLICENSE1",
            allowed_batteries=3,
            user_recharge=1000,
            admin_flag=False,
        )
        self.assertIsInstance(self.user2, Users)

        self.user1.delete()
        self.user2.delete()
