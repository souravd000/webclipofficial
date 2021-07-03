from django.urls import path
from chatclip.views import Inbox, Directs, SendDirect, UserSearch, NewConversation


urlpatterns = [
    path('', Inbox, name='inbox'),
    path('inbox/<username>', Directs, name='directs'),
    path('send/', SendDirect, name='send_direct'),
    path('new/', UserSearch, name='usersearch'),
    path('new/<username>', NewConversation, name='newconversation'),
]