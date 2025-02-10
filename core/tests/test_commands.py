# your_app_name/tests/test_commands.py
from django.core.management import call_command
from django.test import TestCase
from core.models import Country

class PopulateCountriesCommandTests(TestCase):
    def test_populate_countries(self):
        call_command('populate_countries')
        self.assertEqual(Country.objects.count(), 195)