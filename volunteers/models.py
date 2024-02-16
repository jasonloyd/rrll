from django.db import models


class Volunteer(models.Model):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email_address = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    background_check_status = models.CharField(max_length=20, default="pending")
    abuse_awareness_certificate = models.FileField(upload_to="tmp/certificates")
