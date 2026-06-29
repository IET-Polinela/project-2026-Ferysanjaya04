from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Home & Reports (CBV)
    path('', views.home, name='home'),
    path('search/', views.report_search, name='search_report'),
    path('reports/search/', views.report_search, name='report_search'),
    path('reports/', views.ReportListView.as_view(), name='report_list'),
    path('reports/add/', views.ReportCreateView.as_view(), name='add_report'),
    path('reports/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('reports/<int:pk>/edit/', views.ReportUpdateView.as_view(), name='update_report'),
    path('reports/<int:pk>/edit/', views.ReportUpdateView.as_view(), name='edit_report'),
    path('reports/<int:pk>/delete/', views.ReportDeleteView.as_view(), name='delete_report'),
    path('reports/<int:pk>/update-status/', views.ReportUpdateStatusView.as_view(), name='update_status'),
]
