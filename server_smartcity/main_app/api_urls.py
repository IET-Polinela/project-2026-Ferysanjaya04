from rest_framework.routers import DefaultRouter
from django.urls import path
from .api_views import ReportViewSet, public_feed

router = DefaultRouter()
router.register(r'report', ReportViewSet)

urlpatterns = [
    path('report/public-feed/', public_feed, name='public-feed'),
] + router.urls