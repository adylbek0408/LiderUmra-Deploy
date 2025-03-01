from django.contrib import admin
from .models import Manager, Client
from django.utils.translation import gettext_lazy as _


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'status', 'created_at', 'manager', 'package_location']
    list_filter = ('status', 'country', 'city', 'manager', 'created_at', 'package__place')  
    search_fields = ['full_name', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ('status',)

    def formatted_phone(self, obj):
        return obj.phone.format_as("international")
        
    def package_location(self, obj):
        return obj.package.place if obj.package else "-"
    package_location.short_description = 'Филиал'


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'branch', 'formatted_phone')

    def formatted_phone(self, obj):
        return obj.phone.format_as("international")

    formatted_phone.short_description = _('Телефон')
