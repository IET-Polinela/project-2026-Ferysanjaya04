from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from functools import wraps


def admin_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Silakan login terlebih dahulu.")
            return redirect('login')

        is_admin = request.user.is_staff or getattr(request.user, 'is_admin', False)
        if is_admin:
            return view_func(request, *args, **kwargs)

        messages.error(request, "Akses ditolak! Fitur ini hanya untuk Admin.")

        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.path.startswith('/api/'):
            return JsonResponse({'detail': 'Akses ditolak. Fitur ini hanya untuk Admin.'}, status=403)

        return redirect('home')

    return _wrapped_view
