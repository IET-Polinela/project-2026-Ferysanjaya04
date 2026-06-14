from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

# Import decorator custom kita
from usermanagement_23758041.decorators import admin_only
from .models import Report
from .forms import ReportForm, LoginForm, RegisterForm


def is_admin_user(user):
    return user.is_staff or getattr(user, 'is_admin', False)


# --- FUNCTION BASED VIEWS ---

@login_required(login_url='login')
def home(request):
    if is_admin_user(request.user):
        reports = Report.objects.exclude(status='DRAFT')
    else:
        reports = Report.objects.filter(Q(reporter=request.user) | ~Q(status='DRAFT'))

    context = {
        'reports': reports,
        'total_reports': reports.count(),
    }
    return render(request, 'home.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username atau password salah!')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Berhasil logout!')
    return redirect('login')

# Proteksi Admin untuk update status manual
@login_required
@admin_only
def update_status(request, id):
    report = get_object_or_404(Report, id=id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status:
            if not report.can_move_to_status(status):
                messages.error(request, 'Status tidak boleh mundur.')
                return redirect('report_detail', id=report.id)

            report.status = status
            report.save()
            messages.success(request, 'Status berhasil diperbarui!')
    return redirect('report_detail', id=report.id)


# --- CLASS BASED VIEWS (PROTECTED) ---

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'report_list.html'
    context_object_name = 'reports'
    login_url = 'login'

    def get_queryset(self):
        if is_admin_user(self.request.user):
            return Report.objects.exclude(status='DRAFT').order_by('-created_at')

        return Report.objects.filter(
            Q(reporter=self.request.user) | ~Q(status='DRAFT')
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_reports'] = self.get_queryset().count()
        return context

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'report_detail.html'
    context_object_name = 'report'
    pk_url_kwarg = 'id'
    login_url = 'login'

    def get_queryset(self):
        if is_admin_user(self.request.user):
            return Report.objects.exclude(status='DRAFT')

        return Report.objects.filter(
            Q(reporter=self.request.user) | ~Q(status='DRAFT')
        )

class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'add_report.html'
    success_url = reverse_lazy('home')
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        if is_admin_user(request.user):
            messages.error(request, 'Admin tidak boleh membuat laporan.')
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.reporter = self.request.user
        messages.success(self.request, 'Laporan berhasil dibuat!')
        return super().form_valid(form)

class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'edit_report.html'
    pk_url_kwarg = 'id'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        report = self.get_object()

        if is_admin_user(request.user):
            messages.error(request, 'Admin hanya boleh mengubah status laporan.')
            return redirect('report_detail', id=report.id)

        if report.reporter != request.user:
            messages.error(request, 'Anda hanya boleh mengedit laporan sendiri.')
            return redirect('report_detail', id=report.id)

        if report.status != 'DRAFT':
            messages.error(request, 'Laporan yang sudah diajukan hanya bisa dilihat.')
            return redirect('report_detail', id=report.id)

        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        messages.success(self.request, 'Laporan berhasil diperbarui!')
        return reverse_lazy('report_detail', kwargs={'id': self.object.id})

class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'delete_report.html'
    success_url = reverse_lazy('report_list')
    pk_url_kwarg = 'id'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        report = self.get_object()

        if is_admin_user(request.user):
            messages.error(request, 'Admin tidak boleh menghapus laporan.')
            return redirect('report_detail', id=report.id)

        if report.reporter != request.user:
            messages.error(request, 'Anda hanya boleh menghapus laporan sendiri.')
            return redirect('report_detail', id=report.id)

        if report.status != 'DRAFT':
            messages.error(request, 'Laporan yang sudah diajukan tidak boleh dihapus.')
            return redirect('report_detail', id=report.id)

        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Laporan berhasil dihapus!')
        return super().delete(request, *args, **kwargs)

# Proteksi Update Status (Hanya Admin)
@method_decorator([login_required, admin_only], name='dispatch')
class ReportUpdateStatusView(View):
    def post(self, request, id):
        report = get_object_or_404(Report, id=id)
        new_status = request.POST.get('status')
        if new_status and new_status in dict(Report.STATUS_CHOICES):
            if not report.can_move_to_status(new_status):
                messages.error(request, 'Status tidak boleh mundur.')
                return redirect('report_detail', id=report.id)

            report.status = new_status
            report.save()
            messages.success(request, 'Status laporan berhasil diubah!')
        return redirect('report_detail', id=report.id)
    
    # Tambahkan ini di paling bawah main_app/views.py
def register_view(request):
    # Jika Mas sudah punya register di usermanagement, 
    # fungsi ini bisa di-redirect saja ke sana
    return redirect('register')
