from rest_framework import generics
from .models import Mailing, Client, Message
from .serializers import ClientSerializer, MailingSerializer, MessageSerializer, \
    MessageRUDSerializer, MessagePostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .defs import start_mailing
from django.utils import timezone


class ClientListCreateAPIView(generics.ListCreateAPIView):
    # http://127.0.0.1:8000/client_list_create/
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    # http://127.0.0.1:8000/client/detail/<int:client_id>/
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class NewMailingView(APIView):
    # http://127.0.0.1:8000/mailing/create/

    # example of giving information
    # {
    #   "start_date": "2023-05-11 12:32:00",
    #   "end_date": "2023-05-12 12:32:00",
    #   "code_filter": 4321,
    #   "message": "message"
    # }

    def post(self, request):
        data = request.data
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        code_filter = data['code_filter']
        message = data['message']

        # Создание новой рассылки
        mailing = Mailing.objects.create(
            start_date=start_date,
            end_date=end_date,
            code_filter=code_filter,
            message=message
        )

        clients = Client.objects.filter(code_number=code_filter)

        # Отправка сообщений клиентам
        for client in clients:
            current_time = timezone.now()
            if start_date <= current_time <= end_date:
                Message.objects.create(
                    start_date=current_time,
                    mailing_id=mailing,
                    client_id=client,
                    status=1  # Проверка активности
                )
        return Response({'status': 'success'})


class NewFutureMailingView(APIView):
    # http://127.0.0.1:8000/mailing/create_in_future/

    # example of giving information
    # {
    #   "start_date": "2023-05-11 12:32:00",
    #   "end_date": "2023-05-12 12:32:00",
    #   "code_filter": 4321,
    #   "message": "message"
    # }

    def post(self, request):
        serializer = MailingSerializer(data=request.data)
        if serializer.is_valid():
            mailing = serializer.save()
            current_time = timezone.now()
            if mailing.start_date > current_time:
                start_mailing.apply_async(args=[mailing.id], eta=mailing.start_date)
            return Response({'status': 'success'})
        return Response({'status': 'error'})


class MailingRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    # http://127.0.0.1:8000/mailing/detail/<int:mail_id>/
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MessageListAPIView(generics.ListAPIView):
    # http://127.0.0.1:8000/message/list/
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(status=1)
        return qs


class MessageRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    # http://127.0.0.1:8000/message/detail/<int:message_id>/
    queryset = Message.objects.all()
    serializer_class = MessageRUDSerializer


class MessageCreateAPIView(generics.CreateAPIView):
    # http://127.0.0.1:8000/message/create/
    queryset = Message.objects.all()
    serializer_class = MessagePostSerializer