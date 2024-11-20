from core.permissions import IsOwnProfile
from core.models import User
from rest_framework import generics
from .serializers import RegisterUserSerializer, FetchAllUserFieldsSerializer, EditUserProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


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