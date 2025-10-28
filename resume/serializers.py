from typing import Type, Any

from rest_framework import serializers
from .models import JobSubmission


class JobSubmissionSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    """Serializer for job submissions"""
    
    class Meta:
        model = JobSubmission
        fields = ['id', 'title', 'company', 'url', 'description', 'submitted_by', 'submitted_at', 'status']
        read_only_fields = ['id', 'submitted_at', 'status']


class JobSubmissionCreateSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    """Serializer for creating job submissions (simplified fields for public use)"""
    
    class Meta:
        model = JobSubmission
        fields = ['title', 'company', 'url', 'description', 'submitted_by']
        extra_kwargs = {
            'description': {'required': False, 'allow_blank': True},
        }

