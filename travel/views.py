from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .interfaces import TRAVEL_PROVIDER_INTERFACES
from .serializers import TravelQuoteSerializer
from .models import TravelInsurance
from insurance.models import InsuranceProvider

# Create your views here.
class GetTravelInsuranceQuotesView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = TravelQuoteSerializer(data=request.data)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Save the validated data to the database
            travel_insurance = TravelInsurance.objects.create(**validated_data)
            response = {"quote_id": travel_insurance.id, "quotes": []}

            providers = InsuranceProvider.objects.filter(is_active=True, provides_travel=True)
            for provider in providers:
                interface = TRAVEL_PROVIDER_INTERFACES.get(provider.interface)
                if interface:
                    try:
                        api_response = interface.fetch_quote(validated_data)
                        response["quotes"].append(api_response)
                    except Exception as e:
                        # TODO log exception
                        pass

            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)