from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message


# сигнал нужен для статистики, каждая отправка сообщений добавляет в field sent_count единицу
@receiver(post_save, sender=Message)
def update_sent_count(sender, instance, created, *args, **kwargs):
    if created:
        instance.mailing.sent_count += 1
        instance.mailing.save(update_fields=['sent_count'])