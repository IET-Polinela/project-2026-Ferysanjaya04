from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

# Import decorator custom kita
from usermanagement_23758041.decorators import admin_only
from .models import Report
from .forms import ReportForm, LoginForm, RegisterForm

# --- FUNCTION BASED VIEWS ---

@login_required(login_url='login')
def home(request):
    reports = Report.objects.all()
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_reports'] = Report.objects.count()
        return context

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'report_detail.html'
    context_object_name = 'report'
    pk_url_kwarg = 'id'
    login_url = 'login'

# Proteksi Tambah Laporan (Hanya Admin)
@method_decorator([login_required, admin_only], name='dispatch')
class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'add_report.html'
    success_url = reverse_lazy('home')
    login_url = 'login'
    
    def form_valid(self, form):
        messages.success(self.request, 'Laporan berhasil dibuat!')
        return super().form_valid(form)

# Proteksi Edit Laporan (Hanya Admin)
@method_decorator([login_required, admin_only], name='dispatch')
class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'edit_report.html'
    pk_url_kwarg = 'id'
    login_url = 'login'
    
    def get_success_url(self):
        messages.success(self.request, 'Laporan berhasil diperbarui!')
        return reverse_lazy('report_detail', kwargs={'id': self.object.id})

# Proteksi Hapus Laporan (Hanya Admin)
@method_decorator([login_required, admin_only], name='dispatch')
class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'delete_report.html'
    success_url = reverse_lazy('report_list')
    pk_url_kwarg = 'id'
    login_url = 'login'
    
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
            report.status = new_status
            report.save()
            messages.success(request, 'Status laporan berhasil diubah!')
        return redirect('report_detail', id=report.id)
    
    # Tambahkan ini di paling bawah main_app/views.py
def register_view(request):
    # Jika Mas sudah punya register di usermanagement, 
    # fungsi ini bisa di-redirect saja ke sana
    return redirect('register')