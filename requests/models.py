from django.db import models
from django.conf import settings

class Request(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    DOCUMENT_TYPES = [
        ('FP', 'Funding Proposal'),
        ('IL', 'Introduction Letter'),
        ('AL', 'Assignment Letter'),
        ('RL', 'Recommendation Letter'),
        ('AR', 'Access Request'),
        ('OT', 'Other Document'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    date_submitted = models.DateField(auto_now_add=True)  # Non-editable
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_requests")
    deadline = models.DateField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)

    # Field baru untuk admin
    fileadmin = models.FileField(upload_to='admin_files/', blank=True, null=True)
    deskripsiadmin = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

class Attachment(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name