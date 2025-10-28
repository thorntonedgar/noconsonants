from typing import Type, Any, Union, cast

from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.cache import cache
from django.db.models import Q
from .models import JobSubmission
from .serializers import JobSubmissionSerializer, JobSubmissionCreateSerializer


class JobSubmissionViewSet(viewsets.ModelViewSet):  # type: ignore[type-arg]
    """
    API endpoint for job submissions.
    Allows users to submit job opportunities and view their status.
    
    Version 1 of the API.
    """
    queryset = JobSubmission.objects.all()
    permission_classes = [AllowAny]
    
    def get_queryset(self) -> Any:
        """
        Optimize queryset with only() to reduce data transfer.
        Add filtering support.
        """
        queryset = JobSubmission.objects.only(
            'id', 'title', 'company', 'url', 'description', 
            'submitted_by', 'submitted_at', 'status'
        ).all()
        
        # Optional filtering
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def get_serializer_class(self) -> Type[serializers.BaseSerializer[Any]]:
        """Use different serializers for create vs retrieve"""
        if self.action == 'create':
            return JobSubmissionCreateSerializer
        return JobSubmissionSerializer
    
    def list(self, request: Request) -> Response:
        """
        GET /api/jobs/ or GET /api/v1/jobs/
        Retrieve all job submissions (paginated).
        
        Query params:
        - status: Filter by status (pending, applied, interviewing, rejected, accepted)
        """
        # Pagination is handled by REST_FRAMEWORK settings
        jobs = self.get_queryset()
        serializer = JobSubmissionSerializer(jobs, many=True)
        return Response(serializer.data)
    
    def create(self, request: Request) -> Response:
        """
        POST /api/jobs/ or POST /api/v1/jobs/
        Submit a new job opportunity.
        
        Expected payload:
        {
            "title": "Software Engineer",
            "company": "Example Corp",
            "url": "https://example.com/jobs/123",
            "description": "Looking for a Django expert...",
            "submitted_by": "user@example.com"
        }
        
        Includes duplicate detection to prevent spam.
        """
        # Check for recent duplicate submissions to prevent spam
        title = request.data.get('title', '')
        company = request.data.get('company', '')
        
        # Check cache for duplicate submissions in last hour
        duplicate_key = f'job_submission_{title.lower()}_{company.lower()}'
        if cache.get(duplicate_key):
            return Response(
                {'error': 'A similar job was recently submitted. Please wait before submitting again.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        serializer = JobSubmissionCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Check for existing duplicate in database
            existing = JobSubmission.objects.filter(
                Q(title__iexact=title) & Q(company__iexact=company),
                submitted_at__gte=serializer.validated_data.get('submitted_at', None)
            ).exists()
            
            if existing:
                return Response(
                    {'error': 'This job has already been submitted.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save()
            
            # Cache duplicate key for 1 hour
            cache.set(duplicate_key, True, 60 * 60)
            
            return Response(
                {
                    'message': 'Job submission received successfully! Thank you for thinking of me.',
                    'data': serializer.data,
                    'api_version': 'v1'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request: Request, pk: Union[str, int, None] = None) -> Response:
        """
        GET /api/jobs/{id}/ or GET /api/v1/jobs/{id}/
        Retrieve a specific job submission by ID.
        """
        try:
            key: int | str
            if isinstance(pk, str):
                key = int(pk) if pk.isdigit() else pk
            else:
                key = cast(Union[int, str], pk)
            job = JobSubmission.objects.get(pk=key)
            serializer = JobSubmissionSerializer(job)
            response_data = serializer.data
            response_data['api_version'] = 'v1'
            return Response(response_data)
        except JobSubmission.DoesNotExist:
            return Response(
                {'error': 'Job submission not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

