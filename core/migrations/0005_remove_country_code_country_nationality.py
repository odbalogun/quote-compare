# Generated by Django 5.1.3 on 2025-02-05 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_country_passwordresetrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='code',
        ),
        migrations.AddField(
            model_name='country',
            name='nationality',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='nationality'),
        ),
    ]
