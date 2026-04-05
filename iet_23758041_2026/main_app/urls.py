from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Home & Reports
    path('', views.home, name='home'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/add/', views.add_report, name='add_report'),
    path('reports/<int:id>/', views.report_detail, name='report_detail'),
    path('reports/<int:id>/edit/', views.edit_report, name='edit_report'),
    path('reports/<int:id>/delete/', views.delete_report, name='delete_report'),
]