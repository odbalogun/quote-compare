from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from insurance.models import InsuranceProvider
from core.models import User
from life.models import LifeInsurance


class GetLifeInsuranceQuoteViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.provider = InsuranceProvider.objects.create(
            name="Test Provider",
            interface="test_interface",
            provides_life=True,
            is_active=True,
        )

    def test_get_life_insurance_quotes(self):
        url = reverse("get-life-insurance-quotes")
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
            "nok_phone_number": "111234787463",
            "insured_amount": "1000000"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(LifeInsurance.objects.count(), 1)
        self.assertEqual(response.data["quote_id"], LifeInsurance.objects.get().id)