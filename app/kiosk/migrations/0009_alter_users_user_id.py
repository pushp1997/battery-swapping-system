# Generated by Django 4.1.3 on 2022-11-22 18:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("kiosk", "0008_remove_users_user_balance_users_user_recharge_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="user_id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]