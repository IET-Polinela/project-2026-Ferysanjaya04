from rest_framework.routers import DefaultRouter
from .api_views import ReportViewSet

router = DefaultRouter()
router.register(r'report', ReportViewSet)

urlpatterns = router.urls