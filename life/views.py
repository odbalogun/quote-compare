from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from insurance.models import InsuranceProvider
from rest_framework import status
from rest_framework.views import APIView
from .serializers import LifeQuoteSerializer
from core.interfaces import LIFE_PROVIDER_INTERFACES
import logging

logger = logging.getLogger('backend')

# Create your views here.
class GetLifeInsuranceQuoteView(APIView):
    permission_classes = [IsAuthenticated] # TODO remove this. let people get quotes without singing up
    def post(self, request, *args, **kwargs):
        serializer = LifeQuoteSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data

            life_insurance = serializer.save(owner=request.user)
            response = {"quote_id": life_insurance.id, "quotes": []}

            providers = InsuranceProvider.objects.filter(is_active=True, provides_life=True)
            for provider in providers:
                interface = LIFE_PROVIDER_INTERFACES.get(provider.interface)
                if interface:
                    try: 
                        api_response = interface.fetch_quote(validated_data)
                        response["quotes"].append(api_response)
                    except (ConnectionError, TimeoutError) as e:
                        logger.error(f"Network error in GetLifeInsuranceQuoteView: {e}")
                        continue
                    except ValueError as e:
                        logger.error(f"Value error in GetLifeInsuranceQuoteView: {e}")
                        continue
                    except Exception as e:
                        logger.error(f"Unexpected error in GetLifeInsuranceQuoteView: {e}")
                        continue
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)