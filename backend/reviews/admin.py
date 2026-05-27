from django.contrib import admin
from .models import ReviewDecision


@admin.register(ReviewDecision)
class ReviewDecisionAdmin(admin.ModelAdmin):
    list_display = ('emission_record', 'decision', 'reviewer_name', 'created_at')
    list_filter = ('decision',)
    search_fields = ('reviewer_name', 'notes')
    readonly_fields = ('created_at',)
