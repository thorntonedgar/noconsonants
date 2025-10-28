from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import JobSubmissionViewSet

# Create router for DRF viewsets
router = DefaultRouter()
router.register(r'jobs', JobSubmissionViewSet, basename='job-submission')

urlpatterns = router.urls

