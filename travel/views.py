from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .interfaces import TRAVEL_PROVIDER_INTERFACES
from .serializers import TravelQuoteSerializer
from insurance.models import InsuranceProvider

# Create your views here.
class GetTravelInsuranceQuotesView(APIView):
    # TODO add a serializer
    # TODO add validation via serializer
    # TODO save in db
    # FIXME ensure response is being sent 
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = TravelQuoteSerializer(data=request.data)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            results = []

            providers = InsuranceProvider.objects.filter(is_active=True, provides_travel=True)
            for provider in providers:
                interface = TRAVEL_PROVIDER_INTERFACES.get(provider.interface)
                if interface:
                    try:
                        response = interface.fetch_quote(validated_data)
                        # TODO save the response to db
                        results.append(response)
                    except Exception as e:
                        # TODO log exception
                        pass

            return Response(results, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)