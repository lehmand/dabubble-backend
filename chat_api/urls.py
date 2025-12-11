from django.urls import path
from .views import BasicChannelListView, CreateChannelView, DetailChannelView, UpdateChannelMemberView, ChannelMessageView, EditChannelMessage, GetOrCreateDmConversationView, DMMessageView, EditDMMessage, ThreadReplyView

urlpatterns = [
    path('channels/basic-channel-list/', BasicChannelListView.as_view(), name='basic-channel-list'),
    path('channels/create-channel/', CreateChannelView.as_view(), name='create-channel'),
    path('channels/channel-detail/<int:pk>/', DetailChannelView.as_view(), name='detail-channel'),
    path('channels/<int:pk>/members/', UpdateChannelMemberView.as_view(), name='update-members'),
    path('channels/<int:pk>/messages/', ChannelMessageView.as_view(), name='create-channel-message'),
    path('message/<int:pk>/', EditChannelMessage.as_view(), name='edit-channel-message'),
    path('dm/<int:user_id>/', GetOrCreateDmConversationView.as_view(), name='get-or-create-dm-conv'),
    path('dm/<int:dm_conversation_id>/messages/', DMMessageView.as_view(), name='post-dm-message'),
    path('dm/message/<int:pk>/', EditDMMessage.as_view(), name='edit-dm-message'),
    path('thread/message/<int:message_id>/', ThreadReplyView.as_view(), name='thread-message'),
]
