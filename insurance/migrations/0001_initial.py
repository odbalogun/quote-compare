# Generated by Django 5.1.3 on 2025-01-23 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InsuranceProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('interface', models.CharField(max_length=255, verbose_name='interface')),
                ('provides_health', models.BooleanField(default=False, verbose_name='provides health insurance')),
                ('provides_auto', models.BooleanField(default=False, verbose_name='provides auto insurance')),
                ('provides_travel', models.BooleanField(default=False, verbose_name='provides travel insurance')),
            ],
        ),
    ]
