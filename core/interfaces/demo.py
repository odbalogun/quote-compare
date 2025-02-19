from .base import ProviderInterface
from unittest.mock import Mock
import requests

class DemoInsurance(ProviderInterface):
    @property
    def base_url(self):
        return "http://test.com"
    
    def authenticate(self):
        return True
    
    def fetch_quote(self, data):
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "quote_id": "12345",
            "premium": 100.0,
            "coverage": "Standard"
        }
        return mock_response.json()

    def purchase_policy(self, data):
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "policy_id": "67890",
            "status": "Purchased",
            "coverage": "Standard"
        }
        return mock_response.json()