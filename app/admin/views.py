from django.shortcuts import render
from rack.models import Rack


def admin_login(request):
    return render(request, "admin/admin_login.html", {})


def admin_dashboard(request):
    rack = Rack()
    stats = rack.rack_stats()
    return render(
        request,
        "admin/admin_dashboard.html",
        {
            "charged_batteries": stats["charged_batteries"],
            "undercharged_batteries": stats["undercharged_batteries"],
            "empty_shelves": stats["empty_shelves"],
        },
    )
