from django.db import models

# create the Kiosk_user table
class Users(models.Model):
    user_id = models.UUIDField(primary_key=True)
    pin = models.IntegerField(max_length=4, null=False)
    name = models.CharField(max_length=45, null=False)
    email_id = models.CharField(max_length=45, unique=True, null=False)
    phone_no = models.CharField(max_length=15, null=False)
    driving_license = models.CharField(max_length=45, null=False)
    battery_deposit_count = models.IntegerField(max_length=5, null=True)
    admin_flag = models.BooleanField(max_length=1, null=False, default="False")
