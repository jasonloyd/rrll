from django.contrib import admin

from .models import Volunteer


class VolunteerAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "middle_name",
        "last_name",
        "email_address",
        "volunteer_role",
        "background_check_status",
        "created_at",
    ]
    list_filter = ["created_at", "background_check_status"]
    search_fields = ["first_name", "last_name"]


admin.site.register(Volunteer, VolunteerAdmin)
