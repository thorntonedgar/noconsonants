from django.db import models


class JobSubmission(models.Model):
    """Job opportunities submitted by users"""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('applied', 'Applied'),
        ('interviewing', 'Interviewing'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]
    
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    url = models.URLField(help_text="Job posting URL")
    description = models.TextField(help_text="Job description or notes", blank=True)
    submitted_by = models.EmailField(help_text="Email of person who submitted this")
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, help_text="Internal notes")
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = "Job Submissions"
    
    def __str__(self) -> str:
        return f"{self.title} at {self.company}"
