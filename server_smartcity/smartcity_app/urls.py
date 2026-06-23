from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django_scalar.views import scalar_viewer
# Import views untuk JWT dari SimpleJWT (Soal No. 2)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/', include('main_app.api_urls')),

    # Endpoint dokumentasi API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/scalar/', scalar_viewer, name='scalar-ui'),

    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),

    path('', include('main_app.urls')),

    path('admin/', admin.site.urls),

    path('auth/', include('usermanagement_23758041.urls')),

    path('dashboard/', include('dashboard_23758041.urls')),

    # ==============================================================================
    # ROUTING ENDPOINT JWT (Sesuai Petunjuk Soal No. 2)
    # ==============================================================================
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
