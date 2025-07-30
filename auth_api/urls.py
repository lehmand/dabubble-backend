from django.urls import path
from .views import RegistrationView, ActivationView

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/<uidb64>/<token>/', ActivationView.as_view())
]
