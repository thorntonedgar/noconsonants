from django.contrib import admin
from .models import JobSubmission


@admin.register(JobSubmission)
class JobSubmissionAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ['title', 'company', 'submitted_by', 'submitted_at', 'status']
    list_filter = ['status', 'submitted_at']
    search_fields = ['title', 'company', 'submitted_by']
    readonly_fields = ['submitted_at']
    date_hierarchy = 'submitted_at'
    ordering = ['-submitted_at']
