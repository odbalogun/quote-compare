# Generated by Django 5.1.3 on 2025-02-05 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_country_code_country_nationality'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='code',
            field=models.CharField(max_length=3, null=True, unique=True, verbose_name='code'),
        ),
    ]
