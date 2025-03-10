# Generated by Django 5.1.3 on 2025-02-05 07:47

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0004_country_passwordresetrequest'),
        ('insurance', '0002_insuranceprovider_is_active'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TravelInsurance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('phone_number', models.CharField(max_length=30, verbose_name='phone number')),
                ('gender', models.CharField(max_length=20, verbose_name='gender')),
                ('date_of_birth', models.DateField(verbose_name='date of birth')),
                ('address', models.TextField(verbose_name='address')),
                ('city', models.CharField(max_length=150, verbose_name='city')),
                ('state', models.CharField(max_length=150, verbose_name='state')),
                ('nok_full_name', models.CharField(max_length=300, verbose_name='next of kin (full name)')),
                ('nok_address', models.TextField(verbose_name='next of kin address')),
                ('nok_relationship', models.CharField(max_length=100, verbose_name='next of kin relationship')),
                ('pre_existing_medical_condition', models.BooleanField(default=False, verbose_name='pre-existing medical condition')),
                ('passport_no', models.CharField(max_length=50, verbose_name='passport number')),
                ('start_date', models.DateField(verbose_name='start date')),
                ('end_date', models.DateField(verbose_name='end date')),
                ('passport_image_path', models.CharField(blank=True, max_length=255, null=True, verbose_name='passport image path')),
                ('policy_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='policy number')),
                ('premium_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='premium amount')),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='total amount')),
                ('status', models.CharField(choices=[('quote', 'Quote'), ('purchased', 'Purchased'), ('expired', 'Expired')], default='quote', max_length=20, verbose_name='status')),
                ('destination_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='travel_insurances', to='core.country')),
                ('insurance_provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='travel_insurances', to='insurance.insuranceprovider')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
