from rest_framework.routers import DefaultRouter
from django.urls import path
from .api_views import ReportViewSet

router = DefaultRouter()
router.register(r'report', ReportViewSet)

urlpatterns = [
    
] + router.urls