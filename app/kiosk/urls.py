from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user/login/", views.user_login, name="user_login"),
    path("user/decode_camera_feed/", views.decode_camera_feed, name="decode_camera_feed"),
    path("user/register/", views.user_registration, name="user_registration"),
    path(
        "user/register/deposit-payment",
        views.user_deposit_payment,
        name="user_deposit_payment",
    ),
    path(
        "user/register/success/", views.user_registration_success, name="user_registration_success"
    ),
    path("user/login/auth/<str:user_id>/", views.qr_scan_success, name="user_login_auth"),
]
