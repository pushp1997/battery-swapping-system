from django.contrib import admin

# Register your models here.

from kiosk.models import Users

from rack.models import Rack

admin.site.register(Users)
admin.site.register(Rack)
