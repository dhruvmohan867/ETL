import hashlib
from django.db import models


class Upload(models.Model):
    SOURCE_TYPES = [
        ('sap_fuel', 'SAP Fuel/Procurement'),
        ('utility', 'Utility Electricity'),
        ('travel', 'Travel Platform'),
    ]

    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    company = models.ForeignKey(
        'emissions.Company',
        on_delete=models.CASCADE,
        related_name='uploads',
    )
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    file_name = models.CharField(max_length=255)
    file_hash = models.CharField(max_length=64)
    row_count = models.PositiveIntegerField(default=0)
    suspicious_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.source_type} — {self.file_name}"

    @staticmethod
    def compute_file_hash(file_obj):
        hasher = hashlib.sha256()
        for chunk in file_obj.chunks():
            hasher.update(chunk)
        file_obj.seek(0)
        return hasher.hexdigest()
