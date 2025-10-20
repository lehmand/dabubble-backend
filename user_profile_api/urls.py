from django.urls import path
from .views import CurrentUserView, UpdateOrDeleteCurrentUserView, UserProfileView, UpdateProfileView

urlpatterns = [
    path('auth-user-info/', CurrentUserView.as_view(), name='auth-info'),
    path('update-auth-user-info/', UpdateOrDeleteCurrentUserView.as_view(), name='update-auth-info'),
    path('userprofile-info/', UserProfileView.as_view(), name='userprofile-info'),
    path('update-userprofile-info/', UpdateProfileView.as_view(), name='update-userprofile-info')
]
