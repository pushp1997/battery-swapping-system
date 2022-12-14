from django.http import HttpResponse
from django.shortcuts import render, redirect
from kiosk.models import Users
from django.forms import Form
from .exception import (
    User_Already_Exists_Email,
    User_Already_Exists_License,
    Invalid_User_Input,
    Payment_Failed,
)
from .utils import CustomUtilities
import string
import qrcode
from io import BytesIO
import cv2
import base64
import uuid
import os
import sys
from rack.models import Rack


from .models import Users


def index(request):
    return render(request, "kiosk/index.html", {})


def user_login(request):
    return render(request, "kiosk/user-login.html", {})


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
        allowed_batteries = int(request.POST.get("deposit-count", ""))
        driving_license = request.POST.get("license", "")
        phone_no = request.POST.get("phone", "")
        pin = request.POST.get("pin", "")

        response = redirect("/kiosk/user/register/deposit-payment/form/")
        response.set_cookie("email", email_id)
        response.set_cookie("name", name)
        response.set_cookie("battery_num", allowed_batteries)
        response.set_cookie("license", driving_license)
        response.set_cookie("phone", phone_no)
        response.set_cookie("pin", pin)
        return response

    # if a GET (or any other method) we'll render a blank form
    return render(request, "kiosk/user-registration.html", {})


# view for battery deposit payment based on the deposit count
def user_deposit_payment(request):
    deposit_for_new_user = False
    payment_success = False

    deposit_amount = request.POST.get("deposit_amount", "")
    card_number = request.POST.get("card_number", "")
    name_on_card = request.POST.get("name_on_card", "")
    cvv = request.POST.get("cvv", "")
    expiry = request.POST.get("expiry", "")

    payment_success = CustomUtilities.paymentsuccess(
        card_number=card_number, name_on_card=name_on_card, cvv=cvv, expiry=expiry
    )

    if payment_success:
        if "battery_num" in request.COOKIES and "email" in request.COOKIES:
            deposit_for_new_user = True
            try:
                u = Users(
                    email_id=request.COOKIES["email"],
                    name=request.COOKIES["name"],
                    allowed_batteries=int(request.COOKIES["battery_num"]),
                    driving_license=request.COOKIES["license"],
                    phone_no=request.COOKIES["phone"],
                    pin=int(request.COOKIES["pin"]),
                )
                u.save()
            except Exception:
                e = sys.exc_info()[0]
                raise User_Already_Exists_Email

            response = redirect(f"/kiosk/user/register/success/{u.user_id}/")

        else:
            userid = request.COOKIES["user_id"]
            newuserid = userid.replace("-", "")
            req_user_data = Users.objects.get(user_id=newuserid)
            allowed_batteries = req_user_data.allowed_batteries + int(request.COOKIES["battery_num"])
            req_user_data.allowed_batteries = allowed_batteries
            req_user_data.save()
            response = redirect(f"/kiosk/user/dashboard/")
        

    else:
        raise Payment_Failed

    if deposit_for_new_user:
        response.delete_cookie("email")
        response.delete_cookie("name")
        response.delete_cookie("battery_num")
        response.delete_cookie("license")
        response.delete_cookie("phone")
        response.delete_cookie("pin")

    return response


def user_deposit_payment_form(request):
    if "battery_num" in request.COOKIES:
        print("IN DEPOSIT FORM: ", request.COOKIES)
        battery_num = int(request.COOKIES["battery_num"])
        response = render(
            request,
            "kiosk/user-deposit-payment.html",
            {"amount": battery_num * 300},
        )
        return response

    return render(request, "kiosk/user-deposit-payment.html", {})


def user_registration_success(request, user_id):
    qr_img = qrcode.make(user_id)
    buffer = BytesIO()
    qr_img.save(buffer, "PNG")
    img_str = base64.b64encode(buffer.getvalue())
    return render(request, "kiosk/user-registration-success.html", {"qr_img": img_str.decode()})


def qr_scan_success(request, user_id):
    response = render(request, "kiosk/qr-scan-success.html", {})
    response.set_cookie("user_id", user_id)
    return response


def wrf_insufficient_balance(request):
    return render(request, "kiosk/wrf-insufficient-balance.html", {})


def wrf_insufficient_batteries(request):
    return render(request, "kiosk/wrf-insufficient-batteries.html", {})


def wrf_insufficient_deposit(request):
    return render(request, "kiosk/wrf-insufficient-deposit.html", {})


def user_dashboard(request):
    user = Users.objects.all()
    userid = request.COOKIES["user_id"]
    newuserid = userid.replace("-", "")
    print("In user dashboard ", newuserid)
    req_user_data = user.get(user_id=newuserid)
    available_balance = req_user_data.user_recharge
    allowed_batteries = req_user_data.allowed_batteries

    rack_stats_dict = Rack().rack_stats()
    charged_batteries = rack_stats_dict.get("charged_batteries")

    return render(
        request,
        "kiosk/user-dashboard.html",
        {
            "charged_batteries": charged_batteries,
            "available_balance": available_balance,
            "allowed_batteries": allowed_batteries,
        },
    )


def battery_success(request):
    return render(request, "kiosk/battery-submission-success.html", {})


def request_battery(request):
    user = Users.objects.all()
    userid = request.COOKIES["user_id"]
    newuserid = userid.replace("-", "")
    req_user_data = user.get(user_id=newuserid)
    allowed_batteries = req_user_data.allowed_batteries

    if request.method == "POST":
        batteries_withdraw = int(request.POST.get("batteries_withdrawal", ""))
        rack_stats_dict = Rack().rack_stats()
        charged_batteries = rack_stats_dict.get("charged_batteries")

        # insufficient available batteries in rack
        if charged_batteries < batteries_withdraw:
            return render(request, "kiosk/wrf-insufficient-batteries.html", {})
        # insufficient deposit
        elif req_user_data.allowed_batteries < batteries_withdraw:
            response = render(request, "kiosk/wrf-insufficient-deposit.html", {"deposit_count":batteries_withdraw-allowed_batteries})
            response.set_cookie("battery_num", batteries_withdraw-allowed_batteries)
            return response
        # insufficience user account balance
        elif req_user_data.user_recharge < batteries_withdraw * 300:
            return render(request, "kiosk/wrf-insufficient-balance.html", {})
        # withdrawal success 
        else:
            # updated number of allowed batteries to withdraw
            req_user_data.allowed_batteries = allowed_batteries - batteries_withdraw
            # request_withdrawal_of_batteries() returns percentage of batteries ejected
            battery_levels_withdrawn = Rack().request_withdrawal_of_batteries(batteries_withdraw)
            # calculating charged amount 
            total_percentage_withdrawn = sum(battery_levels_withdrawn)
            charged_amount = total_percentage_withdrawn * 3 # 1% battery costs 3 euros
            # updated user account balance
            current_available_balance = req_user_data.user_recharge - charged_amount
            req_user_data.user_recharge = current_available_balance
            # saving the changes in the user object
            req_user_data.save()
            
            return render(
                request, 
                "kiosk/withdrawal-request-success.html", 
                {
                    "battery_stats": battery_levels_withdrawn, 
                    "charged_amount": charged_amount, 
                    "available_balance": current_available_balance
                }
            )
       
    else:
        return render(
            request, 
            "kiosk/request-battery.html", 
            {"allowed_batteries": allowed_batteries}
        )


def submit_battery(request):
    if request.method == "POST":
        batteries_submitted = int(request.POST.get("batteries_submission", ""))
        user = Users.objects.all()
        userid = request.COOKIES["user_id"]
        newuserid = userid.replace("-", "")
        req_user_data = user.get(user_id=newuserid)

        rack_stats_dict = Rack().rack_stats()
        empty_shelves = rack_stats_dict.get("empty_shelves")
        if batteries_submitted > empty_shelves:
            return render(request, "kiosk/battery-submission-fail.html", {})

        # request_submission_of_batteries() returns percentage of submitted batteries 
        battery_levels_submitted = Rack().request_submission_of_batteries(batteries_submitted)
        # calculating amount to be returned to the user balance wallet
        total_percentage_submitted = sum(battery_levels_submitted)
        amount_tobe_returned = total_percentage_submitted * 3 # 1% battery costs 3 euros
        # updated user account balance
        req_user_data.user_recharge = req_user_data.user_recharge + amount_tobe_returned
        current_available_balance = req_user_data.user_recharge
        # updating the number of allowed of batteries to withdraw 
        allowed_batteries = req_user_data.allowed_batteries 
        allowed_batteries += batteries_submitted
        req_user_data.allowed_batteries = allowed_batteries
        # saving the changes in the user object
        req_user_data.save()
        return render(
            request, 
            "kiosk/battery-submission-success.html", 
            {
                "battery_stats":battery_levels_submitted, 
                "amount_returned":amount_tobe_returned, 
                "available_balance":current_available_balance
            }
        )

    # if a GET (or any other method) we'll create a blank form
    return render(request, "kiosk/submit_battery.html", {})


def recharge_payment(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        recharge_amount = request.POST.get("recharge_amount", "")
        card_number = request.POST.get("card_number", "")
        name_on_card = request.POST.get("name_on_card", "")
        cvv = request.POST.get("cvv", "")
        expiry = request.POST.get("expiry", "")

        userid = request.COOKIES["user_id"]
        newuserid = userid.replace("-", "")
        req_user = Users.objects.get(user_id=newuserid)
        userRecharge = req_user.user_recharge
        available_balance = userRecharge + int(recharge_amount)
        req_user.user_recharge = available_balance
        req_user.save()
        return redirect("/kiosk/user/dashboard/")

    # if a GET (or any other method) we'll create a blank form
    return render(request, "kiosk/user-recharge-payment.html", {})


def withdraw_success(request):
    return render(request, "kiosk/withdrawal-request-success.html", {})


def battery_submission_fail(request):
    return render(request, "kiosk/battery-submission-fail.html", {})

