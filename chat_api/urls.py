from django.urls import path
from .views import BasicChannelListView, CreateChannelView

urlpatterns = [
    path('channels/basic-channel-list/', BasicChannelListView.as_view(), name='basic-channel-list'),
    path('channels/create-channel/', CreateChannelView.as_view(), name='create-channel'),
]