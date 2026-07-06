from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

# Import decorator custom kita
from usermanagement_23758041.decorators import admin_only
from .models import Report
from .forms import ReportForm, LoginForm, RegisterForm


def is_admin_user(user):
    return user.is_staff or getattr(user, 'is_admin', False)


def get_post_login_redirect(request, default_name='home'):
    redirect_to = request.POST.get('next') or request.GET.get('next')
    if redirect_to and url_has_allowed_host_and_scheme(
        redirect_to,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(redirect_to)

    if request.user.is_authenticated and is_admin_user(request.user):
        return redirect('dashboard')

    return redirect(default_name)


# --- FUNCTION BASED VIEWS ---

def home(request):
    if not request.user.is_authenticated:
        login_url = reverse('login')
        next_url = request.get_full_path()
        return redirect(f'{login_url}?next={next_url}')

    if is_admin_user(request.user):
        return redirect('dashboard')

    reports = Report.objects.filter(Q(reporter=request.user) | ~Q(status='DRAFT'))
    context = {
        'reports': reports,
        'total_reports': reports.count(),
    }
    return render(request, 'main_app/home.html', context)


def report_detail_api(request, id):
    report = get_object_or_404(Report, id=id)
    return JsonResponse({
        'id': report.id,
        'title': report.title,
        'category': report.category,
        'description': report.description,
        'location': report.location,
        'status': report.status,
    })


def report_search(request):
    if not request.user.is_authenticated or not is_admin_user(request.user):
        return HttpResponseForbidden()

    query = request.GET.get('q', '')
    reports = Report.objects.all()
    if query:
        reports = reports.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
    return JsonResponse({
        'results': [
            {
                'id': report.id,
                'title': report.title,
                'category': report.get_category_display(),
                'location': report.location,
                'status': report.status,
            }
            for report in reports
        ]
    })

def login_view(request):
    if request.user.is_authenticated:
        return get_post_login_redirect(request, 'home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return get_post_login_redirect(request, 'home')
            else:
                messages.error(request, 'Username atau password salah!')
    else:
        form = LoginForm()

    next_url = request.GET.get('next') or request.POST.get('next')
    return render(request, 'login.html', {'form': form, 'next': next_url})

def logout_view(request):
    logout(request)
    messages.success(request, 'Berhasil logout!')
    return redirect('login')

# Proteksi Admin untuk update status manual
@login_required(login_url='login')
@admin_only
def update_status(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status:
            if not report.can_move_to_status(status):
                messages.error(request, 'Status tidak boleh mundur.')
                return redirect('report_detail', pk=report.id)

            report.status = status
            report.save()
            messages.success(request, 'Status berhasil diperbarui!')
    return redirect('report_detail', pk=report.id)


# --- CLASS BASED VIEWS (PROTECTED) ---

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'
    login_url = 'login'

    def get_queryset(self):
        if is_admin_user(self.request.user):
            # Admin hanya melihat laporan non-DRAFT
            return Report.objects.exclude(status='DRAFT').order_by('-created_at')
        # Citizen: lihat laporan sendiri + laporan publik (non-DRAFT)
        return Report.objects.filter(
            Q(reporter=self.request.user) | ~Q(status='DRAFT')
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_reports'] = self.get_queryset().count()
        return context

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    context_object_name = 'report'
    pk_url_kwarg = 'pk'
    login_url = 'login'

    def get_queryset(self):
        if is_admin_user(self.request.user):
            # Admin hanya melihat laporan non-DRAFT
            return Report.objects.exclude(status='DRAFT')

        return Report.objects.filter(
            Q(reporter=self.request.user) | ~Q(status='DRAFT')
        )

class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')
    login_url = 'login'

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        messages.success(self.request, 'Laporan berhasil dibuat!')
        return super().form_valid(form)

class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/edit_report.html'
    pk_url_kwarg = 'pk'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        report = self.get_object()

        # Admin TIDAK boleh edit laporan (spek: ❌ Edit draft)
        if is_admin_user(request.user):
            messages.error(request, 'Admin tidak dapat mengedit laporan.')
            return redirect('report_detail', pk=report.id)

        # Citizen hanya boleh edit laporan milik sendiri yang masih DRAFT
        if report.reporter != request.user or report.status != 'DRAFT':
            messages.error(request, 'Anda hanya bisa mengedit laporan draft milik Anda sendiri.')
            return redirect('report_detail', pk=report.id)

        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        messages.success(self.request, 'Laporan berhasil diperbarui!')
        return reverse_lazy('report_list')

class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/delete_report.html'
    success_url = reverse_lazy('report_list')
    pk_url_kwarg = 'pk'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        report = self.get_object()

        # Admin TIDAK boleh hapus laporan (spek: ❌ Hapus draft)
        if is_admin_user(request.user):
            messages.error(request, 'Admin tidak dapat menghapus laporan.')
            return redirect('report_detail', pk=report.id)

        # Citizen hanya boleh hapus laporan milik sendiri yang masih DRAFT
        if report.reporter != request.user or report.status != 'DRAFT':
            messages.error(request, 'Anda hanya bisa menghapus laporan draft milik Anda sendiri.')
            return redirect('report_detail', pk=report.id)

        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Laporan berhasil dihapus!')
        return super().delete(request, *args, **kwargs)

# Proteksi Update Status (Hanya Admin)
@method_decorator([login_required, admin_only], name='dispatch')
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.POST.get('status')
        if new_status and new_status in dict(Report.STATUS_CHOICES):
            if not report.can_move_to_status(new_status):
                messages.error(request, 'Status tidak boleh mundur.')
                return redirect('report_detail', pk=report.id)

            report.status = new_status
            report.save()
            messages.success(request, 'Status laporan berhasil diubah!')
        return redirect('report_detail', pk=report.id)
    
    # Tambahkan ini di paling bawah main_app/views.py
def register_view(request):
    # Jika Mas sudah punya register di usermanagement, 
    # fungsi ini bisa di-redirect saja ke sana
    return redirect('register')
