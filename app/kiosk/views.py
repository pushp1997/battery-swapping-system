from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from kiosk.models import Users
from django.template import RequestContext
import qrcode
from io import BytesIO
import cv2
import base64
import uuid
import os


from .forms import UserForm
from .models import Users


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
        email_id = request.POST.get("email", "")
        name = request.POST.get("name", "")
        battery_deposit_count = int(request.POST.get("deposit-count", ""))
        driving_license = request.POST.get("license", "")
        phone_no = request.POST.get("phone", "")
        pin = request.POST.get("pin", "")

        response = redirect("/kiosk/user/register/deposit-payment/form/")
        response.set_cookie("email", email_id)
        response.set_cookie("name", name)
        response.set_cookie("battery_num", battery_deposit_count)
        response.set_cookie("license", driving_license)
        response.set_cookie("phone", phone_no)
        response.set_cookie("pin", pin)
        return response
    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, "kiosk/user-registration.html", {"form": form})


# view for battery deposit payment based on the deposit count
def user_deposit_payment(request):
    deposit_for_new_user = False

    deposit_amount = request.POST.get("deposit_amount", "")
    card_number = request.POST.get("card_number", "")
    name_on_card = request.POST.get("name_on_card", "")
    cvv = request.POST.get("cvv", "")
    expiry = request.POST.get("expiry", "")

    if "battery_num" in request.COOKIES:
        deposit_for_new_user = True
        u = Users(
            email_id=request.COOKIES["email"],
            name=request.COOKIES["name"],
            battery_deposit_count=int(request.COOKIES["battery_num"]),
            driving_license=request.COOKIES["license"],
            phone_no=request.COOKIES["phone"],
            pin=int(request.COOKIES["pin"]),
        )
        u.save()

    response = redirect(f"/kiosk/user/register/success/{u.user_id}/")

    if deposit_for_new_user:
        response.delete_cookie("email")
        response.delete_cookie("name")
        response.delete_cookie("battery_num")
        response.delete_cookie("license")
        response.delete_cookie("phone")
        response.delete_cookie("pin")

    return response


def user_deposit_payment_form(request):
    form = UserForm()
    if "battery_num" in request.COOKIES:
        print("IN DEPOSIT FORM: ", request.COOKIES)
        battery_num = int(request.COOKIES["battery_num"])
        response = render(
            request,
            "kiosk/user-deposit-payment.html",
            {"amount": battery_num * 300},
        )
        return response

    return render(request, "kiosk/user-deposit-payment.html", {"form": form})


def user_registration_success(request, user_id):
    qr_img = qrcode.make(user_id)
    buffer = BytesIO()
    qr_img.save(buffer, "PNG")
    img_str = base64.b64encode(buffer.getvalue())
    return render(request, "kiosk/user-registration-success.html", {"qr_img": img_str.decode()})


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
    user = Users.objects.all()
    return render(request, "kiosk/user-dashboard.html", {"user": user})


def battery_success(request):
    return render(request, "kiosk/battery-submission-success.html", {})


def request_battery(request):
    return render(request, "kiosk/request-battery.html", {})


def submit_battery(request):
    if request.method == "POST":
        batteries_submitted = request.POST.get("batteries_submission", "")
        return redirect("/kiosk/user/battery/submission/success/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, "kiosk/submit_battery.html", {"form": form})


def recharge_payment(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        recharge_amount = request.POST.get("recharge_amount", "")
        card_number = request.POST.get("card_number", "")
        name_on_card = request.POST.get("name_on_card", "")
        cvv = request.POST.get("cvv", "")
        expiry = request.POST.get("expiry", "")
        return redirect("/kiosk/user/dashboard/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, "kiosk/user-recharge-payment.html", {"form": form})


def withdraw_success(request):
    return render(request, "kiosk/withdrawal-request-success.html", {})
