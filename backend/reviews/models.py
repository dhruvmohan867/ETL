from django.db import models


class ReviewDecision(models.Model):
    DECISION_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    emission_record = models.ForeignKey(
        'emissions.EmissionRecord',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    decision = models.CharField(max_length=10, choices=DECISION_CHOICES)
    reviewer_name = models.CharField(max_length=100)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.decision} — Record #{self.emission_record_id}"
