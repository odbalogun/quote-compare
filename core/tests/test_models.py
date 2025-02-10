from django.test import TestCase
from core.models import Country

class CountryModelTests(TestCase):
    def test_create_country(self):
        country = Country.objects.create(name="Test Country", code="TC", nationality="Test Nationality")
        self.assertEqual(country.name, "Test Country")
        self.assertEqual(country.code, "TC")
        self.assertEqual(country.nationality, "Test Nationality")