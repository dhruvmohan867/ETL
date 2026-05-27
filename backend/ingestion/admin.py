from django.contrib import admin
from .models import Upload


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'source_type', 'company', 'row_count', 'suspicious_count', 'status', 'created_at')
    list_filter = ('source_type', 'status', 'company')
    search_fields = ('file_name',)
    readonly_fields = ('file_hash', 'created_at')
