from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main_app.urls')),
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    path('', include('main_app.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('usermanagement_23758041.urls')),
    path('dashboard/', include('dashboard_23758041.urls')),
]
