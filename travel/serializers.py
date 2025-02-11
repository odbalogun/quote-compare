from rest_framework import serializers
from datetime import date
from .models import TravelInsurance

class TravelInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelInsurance
        fields = '__all__'

class TravelQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelInsurance
        fields = [
            'title', 'first_name', 'last_name', 'email', 'phone_number', 'gender',
            'date_of_birth', 'address', 'city', 'state',
            'nok_full_name', 'nok_address', 'nok_relationship',
            'pre_existing_medical_condition', 'passport_no',
            'start_date', 'end_date', 'passport_image_path', 'destination_country'
        ]
        extra_kwargs = {
            'destination_country': {'required': True}
        }

    def validate(self, data):
        """
        Check that the start date is before the end date.
        """
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError({"end_date": "End date must be after start date."})
        return data
    
    def validate_start_date(self, value):
        if value <= date.today():
            raise serializers.ValidationError("Start date must be in the future.")
        return value
    
    def validate_end_date(self, value):
        if value <= date.today():
            raise serializers.ValidationError("End date must be in the future.")
        return value

    def validate_passport_no(self, value):
        """
        Check that the passport number is alphanumeric.
        """
        if not str(value).isalnum():
            raise serializers.ValidationError("Passport number must be alphanumeric.")
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        if 'owner' not in validated_data:
            if request and hasattr(request, 'user'):
                validated_data['owner'] = request.user
        return super().create(validated_data)