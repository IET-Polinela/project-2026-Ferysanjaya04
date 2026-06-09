from django.urls import path
# Mengubah import agar mengarah ke RegisterView yang ada di api_views.py (Langkah 5)
from .api_views import RegisterView

urlpatterns = [
    # Path ini akan membuat URL API: localhost:8000/auth/register/
    path('register/', RegisterView.as_view(), name='register'),
]