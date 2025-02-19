from django.test import TestCase
from insurance.models import InsuranceProvider
from life.models import LifeInsurance
from core.models import User

class LifeInsuranceModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpassword")
        self.provider = InsuranceProvider.objects.create(
            name="Test Provider",
            interface="test_interface",
            provides_life=True,
            is_active=True
        )

    def test_create_life_insurance(self):
        life_insurance = LifeInsurance.objects.create(
            owner=self.user,
            title="Mr.",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            phone_number="1234567890",
            gender="Male",
            date_of_birth="1990-01-01",
            address="123 Test St",
            city="Test City",
            state="Test State",
            nok_full_name="Next of Kin",
            nok_address="456 Kin St",
            nok_relationship="Brother",
            nok_phone_number="111234787463",
            insured_amount= "1000000",
            insurance_provider=self.provider
        )
        self.assertEqual(life_insurance.owner, self.user)
        self.assertEqual(life_insurance.insurance_provider, self.provider)