from django.test import TestCase
from core.models import User, Country
from insurance.models import InsuranceProvider
from travel.models import TravelInsurance

class TravelInsuranceModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpassword")
        self.country = Country.objects.create(name="Test Country", code="TC", nationality="Test Nationality")
        self.provider = InsuranceProvider.objects.create(
            name="Test Provider",
            interface="test_interface",
            provides_travel=True,
            is_active=True
        )

    def test_create_travel_insurance(self):
        travel_insurance = TravelInsurance.objects.create(
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
            pre_existing_medical_condition=False,
            passport_no="A1234567",
            start_date="2123-12-01",
            end_date="2123-12-31",
            passport_image_path="/path/to/passport.jpg",
            destination_country=self.country,
            insurance_provider=self.provider
        )
        self.assertEqual(travel_insurance.owner, self.user)
        self.assertEqual(travel_insurance.destination_country, self.country)
        self.assertEqual(travel_insurance.insurance_provider, self.provider)