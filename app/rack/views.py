from django.shortcuts import render
from .models import Rack


def index(request):
    context = {"rack": Rack()}
    return render(request, "index.html", context)
