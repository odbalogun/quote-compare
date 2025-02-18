from abc import ABC, abstractmethod

class TravelProviderInterface(ABC):
    
    @property
    @abstractmethod
    def base_url(self):
        pass

    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def fetch_quote(self, data):
        pass

    @abstractmethod
    def purchase_policy(self, data):
        pass