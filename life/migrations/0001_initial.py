# Generated by Django 5.1.3 on 2025-02-18 17:41

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("insurance", "0004_paymentattemptlog"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="LifeInsurance",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=100, verbose_name="title")),
                (
                    "first_name",
                    models.CharField(max_length=150, verbose_name="first name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=150, verbose_name="last name"),
                ),
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="email address"),
                ),
                (
                    "phone_number",
                    models.CharField(max_length=30, verbose_name="phone number"),
                ),
                ("gender", models.CharField(max_length=20, verbose_name="gender")),
                ("date_of_birth", models.DateField(verbose_name="date of birth")),
                ("address", models.TextField(verbose_name="address")),
                ("city", models.CharField(max_length=150, verbose_name="city")),
                ("state", models.CharField(max_length=150, verbose_name="state")),
                (
                    "last_payment_made_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last payment date"
                    ),
                ),
                (
                    "nok_full_name",
                    models.CharField(
                        max_length=300, verbose_name="next of kin (full name)"
                    ),
                ),
                ("nok_address", models.TextField(verbose_name="next of kin address")),
                (
                    "nok_phone_number",
                    models.CharField(max_length=30, verbose_name="phone number"),
                ),
                (
                    "nok_relationship",
                    models.CharField(
                        max_length=100, verbose_name="next of kin relationship"
                    ),
                ),
                (
                    "insured_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="premium amount",
                    ),
                ),
                (
                    "policy_number",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="policy number",
                    ),
                ),
                (
                    "premium_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="premium amount",
                    ),
                ),
                (
                    "service_fee",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="service fee",
                    ),
                ),
                (
                    "tax",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="value added tax",
                    ),
                ),
                (
                    "total_amount",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="total amount",
                    ),
                ),
                (
                    "date_purchased",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="date purchased"
                    ),
                ),
                (
                    "_metadata",
                    models.JSONField(blank=True, null=True, verbose_name="meta data"),
                ),
                (
                    "policy_starts_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="insurance start date"
                    ),
                ),
                (
                    "policy_expires_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="insurance expires at"
                    ),
                ),
                (
                    "next_renewal_attempt_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="renewal attempt at"
                    ),
                ),
                (
                    "insurance_provider",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="life_insurances",
                        to="insurance.insuranceprovider",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
