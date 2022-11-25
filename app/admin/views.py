from django.shortcuts import render
from rack.models import Rack


def admin_login(request):
    return render(request, "admin/admin_login.html", {})


def admin_dashboard(request):
    rack_stats_dict = Rack().rack_stats()
    empty_shelves = rack_stats_dict.get("empty_shelves")
    undercharged_batteries = rack_stats_dict.get("undercharged_batteries")
    charged_batteries = rack_stats_dict.get("charged_batteries")

    return render(
        request,
        "admin/admin_dashboard.html",
        {
            "charged_batteries": charged_batteries,
            "undercharged_batteries": undercharged_batteries,
            "empty_shelves": empty_shelves,
        },
    )
