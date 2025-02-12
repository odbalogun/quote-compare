from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.contenttypes.models import ContentType
from core.models import User, Country
from insurance.models import InsuranceProvider, PolicyPurchaseLog
from travel.models import TravelInsurance
from unittest.mock import Mock, patch
import datetime

class PurchasePolicyViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.country = Country.objects.create(name="Test Country", code="TC", nationality="Test Nationality")
        self.insurance_provider = InsuranceProvider.objects.create(
            name="Test Provider",
            interface="test_interface",
            provides_travel=True,
            is_active=True
        )
        self.quote = TravelInsurance.objects.create(
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
            start_date="2023-12-01",
            end_date="2023-12-31",
            passport_image_path="/path/to/passport.jpg",
            destination_country=self.country,
            insurance_provider=self.insurance_provider
        )

    @patch('insurance.views.TRAVEL_PROVIDER_INTERFACES')
    def test_purchase_policy_success(self, mock_interfaces):
        mock_interface = Mock()
        mock_interface.purchase_policy.return_value = Mock(status=status.HTTP_200_OK)
        mock_interfaces.get.return_value = mock_interface

        url = reverse('purchase-policy')
        data = {
            'insurance_type': 'travel',
            'quote_id': self.quote.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Policy purchased successfully")

        # Check that the policy log was created
        policy_log = PolicyPurchaseLog.objects.get(object_id=self.quote.id)
        self.assertEqual(policy_log.status, PolicyPurchaseLog.Status.SUCCESS)

        # Check that the quote status was updated
        self.quote.refresh_from_db()
        self.assertEqual(self.quote.status, TravelInsurance.Status.POLICY_PURCHASED)
        self.assertIsNotNone(self.quote.date_purchased)

    @patch('insurance.views.TRAVEL_PROVIDER_INTERFACES')
    def test_purchase_policy_failure(self, mock_interfaces):
        mock_interface = Mock()
        mock_interface.purchase_policy.return_value = Mock(status=status.HTTP_400_BAD_REQUEST)
        mock_interfaces.get.return_value = mock_interface

        url = reverse('purchase-policy')
        data = {
            'insurance_type': 'travel',
            'quote_id': self.quote.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Policy purchase failed")

        # Check that the policy log was created
        policy_log = PolicyPurchaseLog.objects.get(object_id=self.quote.id)
        self.assertEqual(policy_log.status, PolicyPurchaseLog.Status.FAILURE)

    @patch('insurance.views.TRAVEL_PROVIDER_INTERFACES')
    def test_purchase_policy_network_error(self, mock_interfaces):
        mock_interface = Mock()
        mock_interface.purchase_policy.side_effect = ConnectionError("Network error")
        mock_interfaces.get.return_value = mock_interface

        url = reverse('purchase-policy')
        data = {
            'insurance_type': 'travel',
            'quote_id': self.quote.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['error'], "Network error occurred")

    @patch('insurance.views.TRAVEL_PROVIDER_INTERFACES')
    def test_purchase_policy_value_error(self, mock_interfaces):
        mock_interface = Mock()
        mock_interface.purchase_policy.side_effect = ValueError("Invalid data")
        mock_interfaces.get.return_value = mock_interface

        url = reverse('purchase-policy')
        data = {
            'insurance_type': 'travel',
            'quote_id': self.quote.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Invalid data provided")

    @patch('insurance.views.TRAVEL_PROVIDER_INTERFACES')
    def test_purchase_policy_unexpected_error(self, mock_interfaces):
        mock_interface = Mock()
        mock_interface.purchase_policy.side_effect = Exception("Unexpected error")
        mock_interfaces.get.return_value = mock_interface

        url = reverse('purchase-policy')
        data = {
            'insurance_type': 'travel',
            'quote_id': self.quote.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['error'], "An unexpected error occurred")

    def test_purchase_policy_invalid_quote_id(self):
        url = reverse('purchase-policy')
        data = {
            'insurance_type': 'travel',
            'quote_id': 99999  # Invalid quote ID
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Invalid quote ID")