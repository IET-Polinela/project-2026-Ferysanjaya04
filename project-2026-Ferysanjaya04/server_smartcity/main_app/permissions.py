from rest_framework import permissions

class IsOwnerAndDraftOrReadOnly(permissions.BasePermission):
    """
    Custom permission untuk memastikan:
    1. Akses Read-Only (GET, HEAD, OPTIONS) diizinkan untuk semua user yang login.
    2. Akses Modifikasi (PUT, PATCH, DELETE) hanya diizinkan untuk pemilik laporan
       DAN status laporan tersebut harus berupa 'DRAFT'.
    """
    def has_object_permission(self, request, view, obj):
        # Jika metodenya adalah GET, HEAD, atau OPTIONS, langsung izinkan (Read-Only)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Jika ingin memodifikasi (PUT/PATCH/DELETE), wajib memenuhi 2 syarat:
        # 1. Pengguna yang me-request adalah pemilik laporan (obj.reporter == request.user)
        # 2. Status laporan tersebut masih 'DRAFT'
        return obj.reporter == request.user and obj.status == 'DRAFT'