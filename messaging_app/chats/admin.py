from django.contrib import admin
from .models import User, Conversation, Message

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name',
                    'email', 'role', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('created_at',)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'created_at')
    filter_horizontal = ('participants',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'conversation', 'sent_at')
    search_fields = ('sender__email', 'conversation__conversation_id')
