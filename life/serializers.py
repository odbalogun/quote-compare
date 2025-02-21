from rest_framework import serializers
from .models import LifeInsurance


class LifeQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeInsurance
        fields = ['title', 'first_name', 'last_name', 'email', 'phone_number', 'gender',
            'date_of_birth', 'address', 'city', 'state',
            'nok_full_name', 'nok_address', 'nok_relationship', 'nok_phone_number', 'insured_amount' ]
        

class LifeInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeInsurance
        fields = '__all__'