# Generated by Django 5.1.3 on 2025-02-14 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("travel", "0006_travelinsurance_last_payment_made_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="travelinsurance",
            name="nok_phone_number",
            field=models.CharField(
                max_length=30, null=True, verbose_name="next of kin phone number"
            ),
        ),
    ]
