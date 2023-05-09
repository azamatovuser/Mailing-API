from celery import shared_task
from django.utils import timezone
from .models import Mailing, Client, Message
from rest_framework.response import Response


# для отправки сообщений в будущем без сторонной помощи ( автоматическо )
@shared_task
def start_mailing(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)
    clients = Client.objects.filter(code_number=mailing.code_filter)

    for client in clients:
        current_time = timezone.now()
        if mailing.start_date <= current_time <= mailing.end_date:
            Message.objects.create(
                start_date=current_time,
                mailing_id=mailing,
                client_id=client,
                status=1
            )
            return Response({'status': 'success'})
    return Response({'status': 'error'})