from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from kiosk.models import Users
import cv2
import base64
import uuid
import os


from .forms import UserForm


def index(request):
    context = {}
    return render(request, "kiosk/index.html", context)


def user_login(request):
    # stream = CameraStreamingWidget()
    # success, _ = stream.camera.read()
    # if success:
    #     status = True
    # else:
    #     status = False
    return render(request, "kiosk/user-login.html", {})


# def decode_camera_feed(request):
#     stream = CameraStreamingWidget()
#     frames = stream.get_frames()
#     return StreamingHttpResponse(frames, content_type="multipart/x-mixed-replace; boundary=frame")


def decode_camera_feed(request):
    detector = cv2.QRCodeDetector()
    frame_ = request.POST.get("image")
    frame_ = str(frame_)
    data = frame_.replace("data:image/jpeg;base64,", "")
    data = data.replace(" ", "+")
    mgdata = base64.b64decode(data)
    with open("./" + str(uuid.uuid1()) + ".jpg", "wb") as f:
        f.write(mgdata)
    data, _, _ = detector.detectAndDecode(cv2.imread(f.name))
    os.remove(f.name)
    if len(data) > 0:
        return HttpResponse(data)
    return HttpResponse("")


def user_registration(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        email = request.POST.get("email", "")
        name = request.POST.get("name", "")
        battery_deposit_count = int(request.POST.get("deposit-count", ""))
        license = request.POST.get("license", "")
        phone = request.POST.get("phone", "")
        password = request.POST.get("pin", "")
        password_confirmation = request.POST.get("confirm-pin", "")
        user_id = str(uuid.uuid1())
        u = Users(user_id, name, email, license, "N", battery_deposit_count, phone, password, 0)
        u.save()
        print("Redirecting to deposit payment")
        return render(
            request, "kiosk/user-deposit-payment.html", {"amount": battery_deposit_count * 300}
        )

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, "kiosk/user-registration.html", {"form": form})


# view for battery deposit payment based on the deposit count
def user_deposit_payment(request):
    # if this is a POST request we need to process the form data
    print("Redirected to deposit payment")
    if request.method == "POST":
        print("inside post logic")
        deposit_amount = request.POST.get("deposit_amount", "")
        card_number = request.POST.get("card_number", "")
        name_on_card = request.POST.get("name_on_card", "")
        cvv = request.POST.get("cvv", "")
        expiry = request.POST.get("expiry", "")
        return redirect("/kiosk/user/register/success/")

    # if a GET (or any other method) we'll create a blank form
    else:
        print("inside get logic")
        form = UserForm()

    return render(request, "kiosk/user-deposit-payment.html", {"form": form})


def user_registration_success(request):
    context = {}
    return render(request, "kiosk/user-registration-success.html", context)


def qr_scan_success(request, user_id):
    print(user_id)
    return render(request, "kiosk/qr-scan-success.html", {})


def wrf_insufficient_balance(request):
    return render(request, "kiosk/wrf-insufficient-balance.html", {})


def wrf_insufficient_batteries(request):
    return render(request, "kiosk/wrf-insufficient-batteries.html", {})


def wrf_insufficient_deposit(request):
    return render(request, "kiosk/wrf-insufficient-deposit.html", {})


def user_dashboard(request):
    return render(request, "kiosk/user-dashboard.html", {})


def battery_success(request):
    return render(request, "kiosk/battery-submission-success.html", {})


def request_battery(request):
    return render(request, "kiosk/request-battery.html", {})


def submit_battery(request):
    return render(request, "kiosk/submit_battery.html", {})


def recharge_payment(request):
    return render(request, "kiosk/user-recharge-payment.html", {})


def withdraw_success(request):
    return render(request, "kiosk/withdrawal-request-success.html", {})
