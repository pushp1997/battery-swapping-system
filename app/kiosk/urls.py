from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user/login/", views.user_login, name="user_login"),
    path("user/decode_camera_feed/", views.decode_camera_feed, name="decode_camera_feed"),
    path("user/register/", views.user_registration, name="user_registration"),
    path(
        "user/register/deposit-payment/",
        views.user_deposit_payment,
        name="user_deposit_payment",
    ),
    path(
        "user/register/success/", views.user_registration_success, name="user_registration_success"
    ),
    path("user/login/auth/<str:user_id>/", views.qr_scan_success, name="user_login_auth"),
    path(
        "user/battery/request/failure/balance/",
        views.wrf_insufficient_balance,
        name="WRF_insufficient_balance",
    ),
    path(
        "user/battery/request/failure/deposit/",
        views.wrf_insufficient_deposit,
        name="WRF_insufficient_deposit",
    ),
    path(
        "user/battery/request/failure/batteries/",
        views.wrf_insufficient_batteries,
        name="WRF_insufficient_batteries",
    ),
    path(
        "user/dashboard/",
        views.user_dashboard,
        name="user_dashboard",
    ),
    path(
        "user/battery/submission/success/",
        views.battery_success,
        name="battery_submission_success",
    ),
    path(
        "user/battery/request/",
        views.request_battery,
        name="request_battery",
    ),
    path(
        "user/battery/submission/",
        views.submit_battery,
        name="submit_battery",
    ),
    path(
        "user/recharge/",
        views.recharge_payment,
        name="recharge_account",
    ),
    path(
        "user/withdraw/success/",
        views.withdraw_success,
        name="withdrawal_success",
    ),
]
