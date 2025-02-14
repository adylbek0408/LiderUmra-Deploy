from django.contrib import admin
from .models import Manager, Client
from django.utils.translation import gettext_lazy as _


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'status', 'created_at', 'manager']
    list_filter = ('status', 'country', 'city', 'manager', 'created_at')  # добавлен manager    
    search_fields = ['full_name', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ('status',)

    def formatted_phone(self, obj):
        return obj.phone.format_as("international")


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'formatted_phone')

    def formatted_phone(self, obj):
        return obj.phone.format_as("international")

    formatted_phone.short_description = _('Телефон')
