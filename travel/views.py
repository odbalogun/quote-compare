from django.http import JsonResponse
from django.views import View
from .interfaces import TRAVEL_PROVIDER_INTERFACES
from insurance.models import InsuranceProvider

# Create your views here.
class GetTravelInsuranceQuotesView(View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        results = []

        providers = InsuranceProvider.objects.filter(is_active=True, provides_travel=True)
        for provider in providers:
            interface = TRAVEL_PROVIDER_INTERFACES.get(provider.interface)
            if interface:
                try:
                    response = interface.fetch_quote(data)
                    results.append(response)
                except Exception as e:
                    # log exception
                    pass

        return JsonResponse(results, safe=False)