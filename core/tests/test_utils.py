from core.utils import calculate_service_fee, calculate_value_added_tax
from django.test import TestCase
from core.constants import MAX_SERVICE_FEE, VAT_TAX


class CalculateValueAddedTaxTest(TestCase):
    def test_calculate_value_added_tax(self):
        value = calculate_value_added_tax(5000)
        tax = 5000 * (VAT_TAX / 100)
        self.assertEqual(value, tax)


class CalculateServiceFeeTest(TestCase):
    def test_less_than_max_service_fee(self):
        value = calculate_service_fee(5000)
        self.assertLess(value, MAX_SERVICE_FEE)

    def test_equal_to_max_service_fee(self):
        value = calculate_service_fee(50000000)
        self.assertEqual(value, MAX_SERVICE_FEE)
