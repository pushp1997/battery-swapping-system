from django.http import HttpResponse


def index(request):
    return HttpResponse("Yeah, its working! Only the page is changed.")
