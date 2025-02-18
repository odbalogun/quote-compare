from rest_framework import generics
from travel.models import TravelInsurance
from core.interfaces import TRAVEL_PROVIDER_INTERFACES
from insurance.models import PolicyPurchaseLog, PaymentAttemptLog
from rest_framework.response import Response
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from core.constants import PolicyStatus
import logging
from django.utils import timezone

logger = logging.getLogger('backend')

class LogPaymentProcessorResponse(generics.CreateAPIView):
    def post(self, request):
        """
        Log the response from the payment processor
        """
        data = request.data
        quote = TravelInsurance.objects.filter(pk=data.get('quote_id')).first()
        if not quote:
            return Response({"error": "Invalid quote ID"}, status=status.HTTP_400_BAD_REQUEST)
        
        content_type = None
        if data.get('insurance_type') == 'travel':
            content_type = ContentType.objects.get_for_model(TravelInsurance)  

        payment_log = PaymentAttemptLog.objects.create(
            user=request.user,
            insurance_provider=quote.insurance_provider,
            content_type=content_type,
            object_id=quote.id,
            action=PaymentAttemptLog.Action.PAYMENT_ATTEMPT,
            status=PaymentAttemptLog.Status.SUCCESS if data.get('status') == 'success' else PaymentAttemptLog.Status.FAILURE,
            response=str(data)
        )
        payment_log.save()

        if payment_log.status == PaymentAttemptLog.Status.SUCCESS:
            quote.status = PolicyStatus.PAID
            quote.last_payment_made_at = timezone.now()
            quote.save()

        # TODO send email receipt
        return Response({"message": "Payment response logged successfully"}, status=status.HTTP_200_OK)

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
                    quote.status = PolicyStatus.POLICY_PURCHASED
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