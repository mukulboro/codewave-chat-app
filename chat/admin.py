from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Chat, ChatMessage


@admin.register(Chat, ChatMessage)
class UniversalAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]


