from django.db import models
from django.db.models.signals import post_save



class Mailing(models.Model):  # рассылки
    id = models.AutoField(primary_key=True)
    start_date = models.DateTimeField()
    message = models.TextField()
    code_filter = models.CharField(max_length=8)
    sent_count = models.IntegerField(default=0)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.message


class Client(models.Model):  # клиент
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=12)
    code_number = models.CharField(max_length=8)
    tag = models.CharField(max_length=50)
    timezone = models.DateTimeField()

    def __str__(self):
        return self.number



class Message(models.Model):  # сообщение
    STATUS = (
        (0, 'Inactive'),
        (1, 'Active'),
    )
    id = models.AutoField(primary_key=True)
    start_date = models.DateTimeField()
    status = models.IntegerField(choices=STATUS, default=0)
    mailing_id = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='mailing_id', null=True, blank=True)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_id', null=True, blank=True)