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

    def test_user_registration(self):
        client = Client()
        response = client.get(reverse("user_registration"))
        self.assertTemplateUsed(response, "kiosk/user-registration.html")

    # def test_user_deposit_payment(self):
    #     client = Client()
    #     response = client.get(reverse("user_deposit_payment"))
    #     self.assertTemplateUsed(response, "kiosk/user-deposit-payment.html")

    # def test_qr_scan_success(self, user_id):
    #     client = Client()
    #     response = client.get(reverse("qr_scan_success"))
    #     self.assertTemplateUsed(response, "kiosk/qr-scan-success.html")

    # def test_user_registration_success(self):
    #     client = Client()
    #     response = client.get(reverse("user_registration_success"))
    #     self.assertTemplateUsed(response, "kiosk/user-registration-success.html")

    def test_wrf_insufficient_balance(self):
        client = Client()
        response = client.get(reverse("WRF_insufficient_balance"))
        self.assertTemplateUsed(response, "kiosk/wrf-insufficient-balance.html")

    def test_wrf_insufficient_deposit(self):
        client = Client()
        response = client.get(reverse("WRF_insufficient_deposit"))
        self.assertTemplateUsed(response, "kiosk/wrf-insufficient-deposit.html")

    def test_wrf_insufficient_batteries(self):
        client = Client()
        response = client.get(reverse("WRF_insufficient_batteries"))
        self.assertTemplateUsed(response, "kiosk/wrf-insufficient-batteries.html")

    # def test_user_dashboard(self):
    #     client = Client()
    #     response = client.get(reverse("user_dashboard"))
    #     self.assertTemplateUsed(response, "kiosk/user-dashboard.html")

    def test_battery_success(self):
        client = Client()
        response = client.get(reverse("battery_submission_success"))
        self.assertTemplateUsed(response, "kiosk/battery-submission-success.html")

    def test_withdraw_successs(self):
        client = Client()
        response = client.get(reverse("withdrawal_success"))
        self.assertTemplateUsed(response, "kiosk/withdrawal-request-success.html")

    def test_battery_submission_fail(self):
        client = Client()
        response = client.get(reverse("battery_submission_fail"))
        self.assertTemplateUsed(response, "kiosk/battery-submission-fail.html")

    def test_recharge_payment(self):
        client = Client()
        response = client.get(reverse("recharge_account"))
        self.assertTemplateUsed(response, "kiosk/user-recharge-payment.html")

    def test_submit_battery(self):
        client = Client()
        response = client.get(reverse("submit_battery"))
        self.assertTemplateUsed(response, "kiosk/submit_battery.html")
