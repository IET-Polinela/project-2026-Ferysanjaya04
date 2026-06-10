from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Pastikan tidak ada duplikasi pendaftaran
if admin.site.is_registered(User):
    admin.site.unregister(User)

class MyUserAdmin(admin.ModelAdmin):
    # Ini kuncinya agar kolom muncul di tabel depan
    list_display = ('username', 'email', 'is_admin', 'is_staff', 'is_superuser')
    
    # Ini agar ada filter di sebelah kanan
    list_filter = ('is_admin', 'is_staff', 'is_superuser')
    
    # Ini agar saat Mas klik User-nya, field is_admin bisa diedit
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active', 'is_superuser')}),
    )

admin.site.register(User, MyUserAdmin)