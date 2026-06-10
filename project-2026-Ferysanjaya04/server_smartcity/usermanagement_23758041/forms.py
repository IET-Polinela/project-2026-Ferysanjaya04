from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CitizenRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # Pilih field apa saja yang mau ditampilkan di form registrasi
        fields = ("username", "email") 

    def save(self, commit=True):
        user = super().save(commit=False)
        # Sesuai instruksi: otomatis is_admin=False
        user.is_admin = False
        user.is_member = True # Opsional, jika ingin otomatis jadi member juga
        if commit:
            user.save()
        return user