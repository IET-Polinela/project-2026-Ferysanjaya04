from django.urls import path
from .views import DashboardView, chart_data, latest_reports, search_report, report_detail

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('chart-data/', chart_data),
    path('latest/', latest_reports),
    path('search/', search_report),
    path('detail/<int:id>/', report_detail),
]