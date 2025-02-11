from django.shortcuts import render
from rest_framework import generics

# Create your views here.
class PurchaseInsuranceView(generics.CreateAPIView):
    def post(self, request):
        """
        Purchase an insurance policy
        """
        # introduce a serializer here
        # serialzier takes quote_id, insurance provider