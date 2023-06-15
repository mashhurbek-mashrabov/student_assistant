from django.contrib import admin
from django.utils.html import format_html

from tutor_bot.models import TutorTelegramUser


@admin.register(TutorTelegramUser)
class TelegramBotUserAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'user_name', 'full_name', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'language', ('created_at', admin.DateFieldListFilter),
                   ('updated_at', admin.DateFieldListFilter)]
    search_fields = ['chat_id']
    readonly_fields = ['chat_id']

    def user_name(self, obj):
        if obj.username:
            return format_html("<a target='_blank' href='https://t.me/{0}'>{1}</a>", obj.username, obj.name)
        return obj.name
