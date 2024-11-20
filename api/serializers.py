from core.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ["id", "email", "password"]
        # extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, password):
        user = self.instance
        errors = dict()

        try:
            validate_password(user=user, password=password)
        except ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(RegisterUserSerializer, self).validate(password)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class FetchAllUserFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EditUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "middle_name", "last_name", "date_of_birth", "nationality"]