from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import User, Country
from insurance.models import InsuranceProvider
from travel.models import TravelInsurance
from core.utils import calculate_service_fee, calculate_value_added_tax
import uuid
import decimal


class ConfirmTravelInsuranceViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("confirm-travel-insurance")
        self.user = User.objects.create_user(
            email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.provider = InsuranceProvider.objects.create(
            name="Test Provider",
            interface="test_interface",
            provides_travel=True,
            is_active=True,
        )
        self.country = Country.objects.create(
            name="Test Country", code="TC", nationality="Test Nationality"
        )
        self.quote = TravelInsurance.objects.create(
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
            owner=self.user,
        )

    def test_without_provider_id(self):
        data = {"premium_amount": 50000, "quote_id": self.quote.id}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_without_valid_quote_id(self):
        data = {"provider_id": self.provider.id, "premium_amount": 50000}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

        data = {
            "provider_id": self.provider.id,
            "premium_amount": 50000,
            "quote_id": uuid.uuid4(),
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_without_valid_premium_amount(self):
        data = {"provider_id": self.provider.id, "quote_id": self.quote.id}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_successful(self):
        data = {
            "premium_amount": 50000,
            "quote_id": self.quote.id,
            "provider_id": self.provider.id,
        }
        total_fee = data['premium_amount'] + calculate_value_added_tax(data['premium_amount']) + calculate_service_fee(data['premium_amount'])
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.quote.id))
        self.assertEqual(decimal.Decimal(response.data['total_amount']), decimal.Decimal(total_fee))
        self.assertEqual(response.data["status"], TravelInsurance.Status.CONFIRMED)


class GetTravelInsuranceQuotesViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.provider = InsuranceProvider.objects.create(
            name="Test Provider",
            interface="test_interface",
            provides_travel=True,
            is_active=True,
        )
        self.country = Country.objects.create(
            name="Test Country", code="TC", nationality="Test Nationality"
        )

    def test_get_travel_insurance_quotes(self):
        url = reverse("get-travel-insurance-quotes")
        data = {
            "title": "Mr.",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "phone_number": "1234567890",
            "gender": "Male",
            "date_of_birth": "1990-01-01",
            "address": "123 Test St",
            "city": "Test City",
            "state": "Test State",
            "nok_full_name": "Next of Kin",
            "nok_address": "456 Kin St",
            "nok_relationship": "Brother",
            "pre_existing_medical_condition": False,
            "passport_no": "A1234567",
            "start_date": "2123-12-01",
            "end_date": "2123-12-31",
            "passport_image_path": "/path/to/passport.jpg",
            "destination_country": self.country.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TravelInsurance.objects.count(), 1)
        self.assertEqual(response.data["quote_id"], TravelInsurance.objects.get().id)
