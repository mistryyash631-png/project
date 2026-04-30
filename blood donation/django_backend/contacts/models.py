from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    contact = models.CharField(max_length=150)
    subject = models.CharField(max_length=150, default="General Enquiry")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.name} ({self.subject})"
