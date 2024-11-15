from django.shortcuts import render
from core.models import User
from rest_framework import generics
from .serializers import UserSerializer, UserAllFieldsSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class FetchAllUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserAllFieldsSerializer
    permission_classes = [AllowAny]