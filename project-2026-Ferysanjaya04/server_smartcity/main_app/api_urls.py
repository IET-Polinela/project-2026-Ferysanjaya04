from rest_framework.routers import DefaultRouter
from django.urls import path
from .api_views import ReportViewSet, register_user

router = DefaultRouter()
router.register(r'report', ReportViewSet)

urlpatterns = [
    path('register/', register_user, name='register_user'),
] + router.urls