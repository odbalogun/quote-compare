from django.contrib import admin
from django.urls import path, include
from core.views import CreateUserView, FetchAllUsersView, EditUserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/register/', CreateUserView.as_view(), name="register"),
    path('api/users', FetchAllUsersView.as_view(), name="users"),
    path('api/users/<int:pk>/profile', EditUserProfileView.as_view(), name="update-profile"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("api-auth/", include("rest_framework.urls"))
]
