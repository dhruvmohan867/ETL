from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name


class EmissionRecord(models.Model):
    SOURCE_TYPES = [
        ('sap_fuel', 'SAP Fuel/Procurement'),
        ('utility', 'Utility Electricity'),
        ('travel', 'Travel Platform'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='emissions')
    upload = models.ForeignKey(
        'ingestion.Upload',
        on_delete=models.CASCADE,
        related_name='records',
        null=True,
        blank=True,
    )
    row_number = models.PositiveIntegerField(null=True, blank=True)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    category = models.CharField(max_length=100)
    raw_value = models.FloatField()
    normalized_value = models.FloatField(null=True, blank=True)
    raw_unit = models.CharField(max_length=50, blank=True, default='')
    normalized_unit = models.CharField(max_length=50, blank=True, default='')
    reporting_date = models.DateField()
    is_suspicious = models.BooleanField(default=False)
    suspicious_reason = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.source_type} — {self.category} — {self.reporting_date}"
