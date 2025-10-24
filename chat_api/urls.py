from django.urls import path
from .views import BasicChannelListView

urlpatterns = [
    path('basic-channel-list/', BasicChannelListView.as_view(), name='basic-channel-list'),
]