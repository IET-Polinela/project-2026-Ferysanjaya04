from django.shortcuts import render, redirect
from .forms import CitizenRegistrationForm
from django.contrib import messages

def register_citizen(request):
    if request.method == 'POST':
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrasi berhasil! Silakan login.')
            return redirect('login') # Pastikan Mas punya name='login' di urls.py
    else:
        form = CitizenRegistrationForm()
    
    return render(request, 'register.html', {'form': form})