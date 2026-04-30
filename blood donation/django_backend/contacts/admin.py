from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "contact", "subject", "created_at")
    search_fields = ("name", "contact", "subject", "message")
    list_filter = ("subject", "created_at")
