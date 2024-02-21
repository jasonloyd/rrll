from django.db import models

VOLUNTEER_ROLES = {
    "BOARDMEMBER": "board member",
    "COACH": "coach",
    "MANAGER": "manager",
    "SCOREKEEPER": "scorekeeper",
    "UMPIRE": "umpire",
}

class Volunteer(models.Model):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email_address = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    background_check_status = models.CharField(max_length=20, default="pending")
    volunteer_role = models.CharField(max_length=12, choices=VOLUNTEER_ROLES, default="UMPIRE")
    order_id = models.IntegerField(blank=True, null=True)
    abuse_awareness_certificate = models.FileField(upload_to="tmp/certificates")

class VolunteerStatusMessage(models.Model):
    received_at = models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        indexes = [
            models.Index(fields=["received_at"]),
        ]
