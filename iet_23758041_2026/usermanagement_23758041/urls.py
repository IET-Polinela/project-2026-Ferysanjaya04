from django.urls import path
from .views import register_citizen

urlpatterns = [
    # path ini akan membuat URL: localhost:8000/auth/register/
    path('register/', register_citizen, name='register'),
]