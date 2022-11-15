from django.http import HttpResponseRedirect
from django.shortcuts import render


from .forms import UserForm


def index(request):
    context = {}
    return render(request, "index.html", context)


def user_registration(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/kiosk/user/register/success/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, "user-registration.html", {"form": form})


def user_registration_success(request):
    context = {}
    return render(request, "user-registration-success.html", context)
