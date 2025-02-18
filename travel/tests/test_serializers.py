
from django.test import TestCase
from core.models import Country
from core.models import User
from travel.serializers import TravelQuoteSerializer

class TravelQuoteSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpassword")
        self.country = Country.objects.create(name="Test Country", code="TC", nationality="Test Nationality")
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
            "nok_relationship": "Parent",
            "nok_phone_number": "111234787463",
            "pre_existing_medical_condition": False,
            "passport_no": "A1234567",
            "start_date": "2123-12-01",
            "end_date": "2123-12-31",
            "passport_image_path": "/path/to/passport.jpg",
            "destination_country": self.country.id
        }

    def test_valid_data(self):
        serializer = TravelQuoteSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_email(self):
        data = self.data.copy()
        data['email'] = 'test'
        
        serializer = TravelQuoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_invalid_start_date(self):
        data = self.data.copy()
        data['start_date'] = '2020-01-01'
        
        serializer = TravelQuoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('start_date', serializer.errors)

    def test_invalid_end_date(self):
        data = self.data.copy()
        data['end_date'] = '2020-01-01'
        
        serializer = TravelQuoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('end_date', serializer.errors)

    def test_end_date_before_start_date(self):
        data = self.data.copy()
        data['start_date'] = '2123-12-31'
        data['end_date'] = '2123-12-01'
        
        serializer = TravelQuoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('end_date', serializer.errors)