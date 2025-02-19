from core.models import User
from django.test import TestCase
from life.serializers import LifeQuoteSerializer

class LifeQuoteSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpassword")
        self.data = {
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

    def test_valid_data(self):
        serializer = LifeQuoteSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_email(self):
        data = self.data.copy()
        data['email'] = 'test'
        
        serializer = LifeQuoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)