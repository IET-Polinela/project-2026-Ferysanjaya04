from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Cek apakah user sudah login dan apakah is_admin-nya True
        if request.user.is_authenticated and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            # Jika bukan admin, kasih pesan error dan lempar balik ke daftar laporan
            messages.error(request, "Akses ditolak! Fitur ini hanya untuk Admin.")
            return redirect('report_list') # Ganti 'report_list' sesuai name url daftar laporan Mas
    return _wrapped_view