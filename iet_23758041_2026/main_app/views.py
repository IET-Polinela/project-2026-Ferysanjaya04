from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Report
from .forms import ReportForm, LoginForm, RegisterForm


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


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Akun berhasil dibuat! Selamat datang!')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Berhasil logout!')
    return redirect('login')


@login_required(login_url='login')
def home(request):
    reports = Report.objects.all()
    context = {
        'reports': reports,
        'total_reports': reports.count(),
    }
    return render(request, 'home.html', context)


# Class-Based Views untuk CRUD Report
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


class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'add_report.html'
    success_url = reverse_lazy('home')
    login_url = 'login'
    
    def form_valid(self, form):
        messages.success(self.request, 'Laporan berhasil dibuat!')
        return super().form_valid(form)


class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'edit_report.html'
    pk_url_kwarg = 'id'
    login_url = 'login'
    
    def get_success_url(self):
        messages.success(self.request, 'Laporan berhasil diperbarui!')
        return reverse_lazy('report_detail', kwargs={'id': self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report'] = self.object
        return context


class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'delete_report.html'
    success_url = reverse_lazy('report_list')
    pk_url_kwarg = 'id'
    login_url = 'login'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Laporan berhasil dihapus!')
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report'] = self.object
        return context


class ReportUpdateStatusView(View):
    """View untuk mengubah status laporan"""
    def post(self, request, id):
        report = get_object_or_404(Report, id=id)
        new_status = request.POST.get('status')
        
        if new_status and new_status in dict(Report.STATUS_CHOICES):
            report.status = new_status
            report.save()
        
        return redirect('report_detail', id=report.id)
