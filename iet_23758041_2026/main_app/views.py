from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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


@login_required(login_url='login')
def report_list(request):
    reports = Report.objects.all()
    context = {
        'reports': reports,
        'total_reports': reports.count()
    }
    return render(request, 'report_list.html', context)


@login_required(login_url='login')
def report_detail(request, id):
    report = get_object_or_404(Report, id=id)
    return render(request, 'report_detail.html', {'report': report})


@login_required(login_url='login')
def add_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Laporan berhasil dibuat!')
            return redirect('home')
    else:
        form = ReportForm()
    return render(request, 'add_report.html', {'form': form})


@login_required(login_url='login')
def edit_report(request, id):
    report = get_object_or_404(Report, id=id)
    if request.method == "POST":
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Laporan berhasil diperbarui!')
            return redirect('report_detail', id=report.id)
    else:
        form = ReportForm(instance=report)
    return render(request, 'edit_report.html', {'form': form, 'report': report})


@login_required(login_url='login')
def delete_report(request, id):
    report = get_object_or_404(Report, id=id)
    if request.method == "POST":
        report.delete()
        messages.success(request, 'Laporan berhasil dihapus!')
        return redirect('report_list')
    return render(request, 'delete_report.html', {'report': report})
