from django.urls import path
from .views import CurrentUserView, UpdateOrDeleteCurrentUser

urlpatterns = [
    path('auth-user-info/', CurrentUserView.as_view(), name='auth-info'),
    path('update-auth-user-info/', UpdateOrDeleteCurrentUser.as_view(), name='update-auth-info'),
]
