from django.contrib import admin

from .models import BloodRequest, ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "contact", "subject", "created_at")
    search_fields = ("name", "contact", "subject", "message")
    list_filter = ("subject", "created_at")


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = (
        "request_id",
        "patient_name",
        "blood_group",
        "units_required",
        "urgency",
        "status",
        "contact_phone",
        "required_by_date",
        "created_at",
    )
    search_fields = (
        "request_id",
        "patient_name",
        "hospital",
        "contact_phone",
        "user_email",
    )
    list_filter = ("urgency", "status", "blood_group", "required_by_date", "created_at")
    readonly_fields = ("request_id", "created_at")


admin.site.site_header = "Life Saver Admin Dashboard"
admin.site.site_title = "Life Saver Admin"
admin.site.index_title = "Blood Donation Management"
