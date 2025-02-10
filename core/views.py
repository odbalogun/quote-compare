from core.permissions import IsOwnProfile
from core.models import User
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer, FetchAllUserFieldsSerializer, EditUserProfileSerializer, CountrySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import Country

class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

class EditUserProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = EditUserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnProfile]

class FetchAllUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = FetchAllUserFieldsSerializer
    permission_classes = [AllowAny]

# class RequestPasswordReset(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         """
#         Logs a password reset request
#         """
#         pass