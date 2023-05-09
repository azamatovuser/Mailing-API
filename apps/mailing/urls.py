from django.urls import path
from .views import ClientListCreateAPIView, ClientRUDAPIView, NewMailingView, \
    MailingRUDAPIView, MessageListAPIView, MessageRUDAPIView, MessageCreateAPIView, NewFutureMailingView


urlpatterns = [
    path('client_list_create/', ClientListCreateAPIView.as_view()),
    path('client/detail/<int:pk>/', ClientRUDAPIView.as_view()),
    path('mailing/create/', NewMailingView.as_view()),
    path('mailing/create_in_future/', NewFutureMailingView.as_view()),
    path('mailing/detail/<int:pk>/', MailingRUDAPIView.as_view()),
    path('message/list/', MessageListAPIView.as_view()),
    path('message/create/', MessageCreateAPIView.as_view()),
    path('message/detail/<int:pk>/', MessageRUDAPIView.as_view()),
]