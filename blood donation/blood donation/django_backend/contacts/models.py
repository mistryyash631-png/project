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


class BloodRequest(models.Model):
    URGENCY_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]
    STATUS_CHOICES = [
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Closed", "Closed"),
    ]

    request_id = models.CharField(max_length=20, unique=True)
    patient_name = models.CharField(max_length=150)
    patient_age = models.PositiveIntegerField(null=True, blank=True)
    hospital = models.CharField(max_length=200)
    ward = models.CharField(max_length=150, blank=True)
    blood_group = models.CharField(max_length=5)
    units_required = models.PositiveIntegerField(default=1)
    required_by_date = models.DateField(null=True, blank=True)
    contact_phone = models.CharField(max_length=30)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default="Medium")
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Open")
    user_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.request_id} - {self.patient_name} ({self.blood_group})"
