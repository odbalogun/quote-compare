from rest_framework import generics
from travel.models import TravelInsurance
from travel.interfaces import TRAVEL_PROVIDER_INTERFACES
from insurance.models import PolicyPurchaseLog
from rest_framework.response import Response
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
import logging
from django.utils import timezone

logger = logging.getLogger('backend')

# Create your views here.
class PurchasePolicyView(generics.CreateAPIView):
    def post(self, request):
        """
        Purchase an insurance policy
        """
        data = request.data
        if data.get('insurance_type') == 'travel':
            quote = TravelInsurance.objects.filter(pk=data.get('quote_id')).first()
            if not quote:
                return Response({"error": "Invalid quote ID"}, status=status.HTTP_400_BAD_REQUEST)
            interface = TRAVEL_PROVIDER_INTERFACES.get(quote.insurance_provider.interface)
            try:
                # call interface to purchase policy
                response = interface.purchase_policy(quote)
                if response.status == status.HTTP_200_OK:
                    # log transaction
                    policy_log = PolicyPurchaseLog.objects.create(
                        user=request.user,
                        insurance_provider=quote.insurance_provider,
                        content_type=ContentType.objects.get_for_model(TravelInsurance),
                        object_id=quote.id,
                        action=PolicyPurchaseLog.Action.PURCHASE,
                        status=PolicyPurchaseLog.Status.SUCCESS,
                        response=str(response.data)
                    )
                    policy_log.save()

                    # update quote status
                    quote.status = TravelInsurance.Status.POLICY_PURCHASED
                    quote.date_purchased = timezone.now()
                    quote.save()

                    # TODO send email
                    return Response({"message": "Policy purchased successfully"}, status=status.HTTP_200_OK)
                else:
                    # log transaction
                    policy_log = PolicyPurchaseLog.objects.create(
                        user=request.user,
                        insurance_provider=quote.insurance_provider,
                        content_type=ContentType.objects.get_for_model(TravelInsurance),
                        object_id=quote.id,
                        action=PolicyPurchaseLog.Action.PURCHASE,
                        status=PolicyPurchaseLog.Status.FAILURE,
                        response=str(response.data)
                    )
                    policy_log.save()
                    return Response({"error": "Policy purchase failed"}, status=status.HTTP_400_BAD_REQUEST)
            except (ConnectionError, TimeoutError) as e:
                logger.error(f"Network error in PurchasePolicyView: {e}")
                return Response({"error": "Network error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except ValueError as e:
                logger.error(f"Value error in PurchasePolicyView: {e}")
                return Response({"error": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error(f"Unexpected error in PurchasePolicyView: {e}")
                return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)