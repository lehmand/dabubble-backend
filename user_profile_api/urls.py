from django.urls import path
from .views import CurrentUserView, UpdateOrDeleteCurrentUser

urlpatterns = [
    path('current-user/', CurrentUserView.as_view(), name='current-user'),
    path('me/', UpdateOrDeleteCurrentUser.as_view(), name='update-user')
]
