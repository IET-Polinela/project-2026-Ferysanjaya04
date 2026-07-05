from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from main_app.models import Report
from usermanagement_23758041.decorators import admin_only
from django.utils.decorators import method_decorator


# ================= DASHBOARD VIEW (Admin Only) =================
@method_decorator([login_required, admin_only], name='dispatch')
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'


# ================= CHART DATA (Admin Only) =================
@login_required
@admin_only
def chart_data(request):
    status_data = Report.objects.values('status').annotate(total=Count('id'))
    category_data = Report.objects.values('category').annotate(total=Count('id'))

    return JsonResponse({
        'status': list(status_data),
        'category': list(category_data),
    })


# ================= TABLE DATA (Admin Only) =================
@login_required
@admin_only
def latest_reports(request):
    reported = Report.objects.filter(status='REPORTED').order_by('-id')[:5]
    resolved = Report.objects.filter(status='RESOLVED').order_by('-id')[:5]

    return JsonResponse({
        'reported': list(reported.values('id', 'title', 'status')),
        'resolved': list(resolved.values('id', 'title', 'status')),
    })


# ================= LIVE SEARCH (Admin Only) =================
@login_required
@admin_only
def search_report(request):
    query = request.GET.get('q', '')

    if query:
        reports = Report.objects.filter(title__icontains=query)
    else:
        reports = Report.objects.all()

    data = list(reports.values('id', 'title', 'status', 'category'))

    return JsonResponse(data, safe=False)


# ================= DETAIL MODAL (Admin Only) =================
@login_required
@admin_only
def report_detail(request, id):
    report = Report.objects.filter(id=id).values(
        'id', 'title', 'description', 'status', 'location'
    ).first()

    if report:
        return JsonResponse(report)
    else:
        return JsonResponse({'error': 'Data tidak ditemukan'}, status=404)