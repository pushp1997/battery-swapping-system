# Generated by Django 4.1.3 on 2022-11-16 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kiosk", "0002_remove_users_admin_flag_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="users",
            name="admin_flag",
            field=models.IntegerField(default=0, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="users",
            name="battery_deposit_count",
            field=models.IntegerField(default=0, max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="users",
            name="phone_no",
            field=models.IntegerField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="users",
            name="pin",
            field=models.IntegerField(default=0, max_length=4),
            preserve_default=False,
        ),
    ]
