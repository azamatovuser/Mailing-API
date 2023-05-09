from django.contrib import admin
from .models import Mailing, Client, Message


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'code_filter', 'start_date', 'end_date')
    date_hierarchy = 'start_date'


@admin.register(Client)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'tag', 'timezone')


admin.site.register(Message)