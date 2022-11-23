from django.test import SimpleTestCase
from django.urls import reverse, resolve
from kiosk.views import (
    index,
    user_login,
    decode_camera_feed,
    user_registration,
    user_deposit_payment_form,
    user_deposit_payment,
    user_registration_success,
    qr_scan_success,
    wrf_insufficient_balance,
    wrf_insufficient_deposit,
    wrf_insufficient_batteries,
    user_dashboard,
    battery_success,
    request_battery,
    submit_battery,
    recharge_payment,
    withdraw_success,
)


class TestUrls(SimpleTestCase):
    def test_kiosk_index_url_is_resolved(self):
        url = reverse("kiosk_index")
        self.assertEquals(resolve(url).func, index)

    def test_user_login_url_is_resolved(self):
        url = reverse("user_login")
        self.assertEquals(resolve(url).func, user_login)

    def test_decode_camera_feed_url_is_resolved(self):
        url = reverse("decode_camera_feed")
        self.assertEquals(resolve(url).func, decode_camera_feed)

    def test_user_registration_url_is_resolved(self):
        url = reverse("user_registration")
        self.assertEquals(resolve(url).func, user_registration)

    def test_user_deposit_payment_form_url_is_resolved(self):
        url = reverse("user_deposit_payment_form")
        self.assertEquals(resolve(url).func, user_deposit_payment_form)

    def test_user_deposit_payment_url_is_resolved(self):
        url = reverse("user_deposit_payment")
        self.assertEquals(resolve(url).func, user_deposit_payment)

    def test_user_registration_success_url_is_resolved(self):
        url = reverse("user_registration_success", args=["testUserId"])
        self.assertEquals(resolve(url).func, user_registration_success)

    def test_user_login_auth_url_is_resolved(self):
        url = reverse("user_login_auth", args=["testUserId"])
        self.assertEquals(resolve(url).func, qr_scan_success)

    def test_WRF_insufficient_balance_url_is_resolved(self):
        url = reverse("WRF_insufficient_balance")
        self.assertEquals(resolve(url).func, wrf_insufficient_balance)

    def test_WRF_insufficient_deposit_url_is_resolved(self):
        url = reverse("WRF_insufficient_deposit")
        self.assertEquals(resolve(url).func, wrf_insufficient_deposit)

    def test_WRF_insufficient_batteries_url_is_resolved(self):
        url = reverse("WRF_insufficient_batteries")
        self.assertEquals(resolve(url).func, wrf_insufficient_batteries)

    def test_user_dashboard_url_is_resolved(self):
        url = reverse("user_dashboard")
        self.assertEquals(resolve(url).func, user_dashboard)

    def test_battery_submission_success_url_is_resolved(self):
        url = reverse("battery_submission_success")
        self.assertEquals(resolve(url).func, battery_success)

    def test_request_battery_url_is_resolved(self):
        url = reverse("request_battery")
        self.assertEquals(resolve(url).func, request_battery)

    def test_submit_battery_url_is_resolved(self):
        url = reverse("submit_battery")
        self.assertEquals(resolve(url).func, submit_battery)

    def test_recharge_account_url_is_resolved(self):
        url = reverse("recharge_account")
        self.assertEquals(resolve(url).func, recharge_payment)

    def test_withdrawal_success_url_is_resolved(self):
        url = reverse("withdrawal_success")
        self.assertEquals(resolve(url).func, withdraw_success)
