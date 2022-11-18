from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user/register/", views.user_registration, name="user_registration"),
    path(
        "user/register/deposit-payment",
        views.user_deposit_payment,
        name="user_deposit_payment",
    ),
    path(
        "user/register/success/", views.user_registration_success, name="user_registration_success"
    ),
]
