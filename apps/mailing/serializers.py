from rest_framework import serializers
from .models import Mailing, Client, Message
from django.utils import timezone


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'number', 'code_number', 'tag', 'timezone']


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ['id', 'start_date', 'message', 'code_filter', 'sent_count', 'end_date']


class MessageSerializer(serializers.ModelSerializer):
    mailing_id = MailingSerializer(read_only=True)
    client_id = ClientSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'start_date', 'status', 'mailing_id', 'client_id']


class MessageRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'start_date', 'status']


class MessagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'start_date', 'status']