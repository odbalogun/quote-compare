from django.contrib import admin
from django.urls import path, include
from core.views import CreateUserView, FetchAllUsersView, EditUserProfileView, CountryListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from travel.views import GetTravelInsuranceQuotesView, ConfirmTravelInsuranceView
from life.views import GetLifeInsuranceQuoteView
from insurance.views import PurchasePolicyView, LogPaymentProcessorResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/register/', CreateUserView.as_view(), name="register-user"),
    path('api/users', FetchAllUsersView.as_view(), name="fetch-all-users"),
    path('api/users/<int:pk>/profile', EditUserProfileView.as_view(), name="edit-user-profile"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("api-auth/", include("rest_framework.urls")),
    path('api/travel/get-quotes/', GetTravelInsuranceQuotesView.as_view(), name='get-travel-insurance-quotes'),
    path('api/travel/confirm-quote/', ConfirmTravelInsuranceView.as_view(), name='confirm-travel-insurance'),
    path('api/countries/', CountryListView.as_view(), name='country-list'),
    path('api/insurance/purchase/', PurchasePolicyView.as_view(), name='purchase-policy'),
    path('api/insurance/paymentlog/', LogPaymentProcessorResponse.as_view(), name='log-payment-response'),
    path('api/life/quotes/', GetLifeInsuranceQuoteView.as_view(), name='get-life-insurance-quotes'),
]
