from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .interfaces import TRAVEL_PROVIDER_INTERFACES
from .serializers import TravelQuoteSerializer, TravelInsuranceSerializer
from .models import TravelInsurance
from insurance.models import InsuranceProvider
from core.utils import calculate_service_fee, calculate_value_added_tax
from core.constants import MAX_SERVICE_FEE
import logging

logger = logging.getLogger('backend')

# Create your views here.
class GetTravelInsuranceQuotesView(APIView):
    permission_classes = [IsAuthenticated] # TODO consider making this available without loggign in
    def post(self, request, *args, **kwargs):
        serializer = TravelQuoteSerializer(data=request.data)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Save the validated data to the database
            travel_insurance = serializer.save(owner=request.user)
            response = {"quote_id": travel_insurance.id, "quotes": []}

            providers = InsuranceProvider.objects.filter(is_active=True, provides_travel=True)
            for provider in providers:
                interface = TRAVEL_PROVIDER_INTERFACES.get(provider.interface)
                if interface:
                    try:
                        api_response = interface.fetch_quote(validated_data)
                        response["quotes"].append(api_response)
                    except (ConnectionError, TimeoutError) as e:
                        logger.error(f"Network error in GetTravelInsuranceQuotesView: {e}")
                        return Response({"error": "Network error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    except ValueError as e:
                        logger.error(f"Value error in GetTravelInsuranceQuotesView: {e}")
                        return Response({"error": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        logger.error(f"Unexpected error in GetTravelInsuranceQuotesView: {e}")
                        return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ConfirmTravelInsuranceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        premium_amount = request.data.get("premium_amount")
        if not premium_amount:
            return Response({"error": "premium_amount is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        provider_id = request.data.get("provider_id")
        provider = InsuranceProvider.objects.filter(pk=provider_id, is_active=True, provides_travel=True).first()
        if not provider:
            return Response({"error": "Invalid provider selected"}, status=status.HTTP_400_BAD_REQUEST)
        
        quote_id = request.data.get("quote_id")
        quote = TravelInsurance.objects.filter(id=quote_id, owner=request.user).first()
        if not quote:
            return Response({"error": "Invalid quote provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            quote.status = TravelInsurance.Status.CONFIRMED
            quote.premium_amount = premium_amount
            quote.service_fee = calculate_service_fee(quote.premium_amount)
            quote.tax = calculate_value_added_tax(quote.premium_amount)
            quote.total_amount = quote.service_fee + quote.premium_amount + quote.tax
            quote.insurance_provider = provider
            quote.save()
            serializer = TravelInsuranceSerializer(quote)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ConnectionError, TimeoutError) as e:
            logger.error(f"Network error in ConfirmTravelInsuranceView: {e}")
            return Response({"error": "Network error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            logger.error(f"Value error in ConfirmTravelInsuranceView: {e}")
            return Response({"error": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error in ConfirmTravelInsuranceView: {e}")
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)