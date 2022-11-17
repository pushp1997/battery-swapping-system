from django.http import HttpResponseRedirect
from django.shortcuts import render


from .forms import UserForm


def index(request):
    context = {}
    return render(request, "kiosk/index.html", context)


def user_registration(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        email = request.POST.get("email", "")
        name = request.POST.get("name", "")
        battery_deposit_count = request.POST.get("deposit-count", "")
        license = request.POST.get("license", "")
        phone = request.POST.get("phone", "")
        password = request.POST.get("pin", "")
        password_confirmation = request.POST.get("confirm-pin", "")
        return HttpResponseRedirect("/kiosk/user/register/deposit-payment/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, "kiosk/user-registration.html", {"form": form})


# view for battery deposit payment based on the deposit count
def user_deposit_payment(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        deposit_amount = request.POST.get("deposit_amount", "")
        card_number = request.POST.get("card_number", "")
        name_on_card = request.POST.get("name_on_card", "")
        cvv = request.POST.get("cvv", "")
        expiry = request.POST.get("expiry", "")
        return HttpResponseRedirect("/kiosk/user/register/success/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, "kiosk/user-deposit-payment.html", {"form": form})


def user_registration_success(request):
    context = {}
    return render(request, "kiosk/user-registration-success.html", context)
