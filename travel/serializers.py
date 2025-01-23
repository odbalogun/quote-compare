from rest_framework import serializers
from .models import TravelInsurance

class TravelQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelInsurance
        fields = []