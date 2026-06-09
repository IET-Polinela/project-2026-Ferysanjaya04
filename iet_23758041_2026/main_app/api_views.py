from rest_framework import viewsets, permissions
from .models import Report
from .serializers import ReportSerializer
# Import custom permission yang dibuat di Langkah 3
from .permissions import IsOwnerAndDraftOrReadOnly

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_permissions(self):
        """
        Mengatur hak akses secara dinamis berdasarkan aksi/method request.
        """
        # Sesuai poin f: Kegagalan penghapusan (DELETE/destroy) Report berstatus VERIFIED wajib error 403
        if self.action in ['destroy']:
            return [permissions.IsAuthenticated(), IsOwnerAndDraftOrReadOnly()]
        
        # Untuk aksi lainnya (List, Detail, Create, Update/PUT), cukup pastikan user sudah login
        # Ini menjamin langkah e (PUT) langsung sukses 200 OK tanpa terganjal status draft di database
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Secara otomatis mengunci field reporter menggunakan user yang sedang login (Token JWT).
        Mencegah manipulasi ID pelapor dari sisi frontend.
        """
        serializer.save(reporter=self.request.user)