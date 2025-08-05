from django.urls import path
from .views import RegistrationView, ActivationView, CookieTokenObtainPairView, CookieTokenRefreshView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/<uidb64>/<token>/', ActivationView.as_view()),
    path('token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
]
