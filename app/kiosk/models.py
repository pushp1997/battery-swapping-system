import uuid
from django.db import models

# create the Kiosk_user table
class Users(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pin = models.IntegerField(null=False)
    name = models.CharField(max_length=45, null=False)
    email_id = models.CharField(max_length=45, unique=True, null=False)
    phone_no = models.CharField(max_length=15, null=False)
    driving_license = models.CharField(max_length=45, null=False, unique=True)
    available_batteries = models.IntegerField(null=True)
    user_recharge = models.IntegerField(null=True, default=0)
    admin_flag = models.BooleanField(null=False, default="False")
