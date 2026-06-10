from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import Report
from .serializers import ReportSerializer, UserRegistrationSerializer
# Import custom permission yang dibuat di Langkah 3
from .permissions import IsOwnerAndDraftOrReadOnly

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_queryset(self):
        """
        LAB 12: Mengoptimalkan API dengan Server-Side Filtering, Sorting, dan Pagination.
        
        Membaca parameter 'tab' dari URL query parameter untuk membedakan:
        - ?tab=my_reports  : Hanya laporan milik user yang sedang login
        - ?tab=feed        : Laporan dari warga lain yang statusnya BUKAN DRAFT
        
        Queryset selalu diurutkan berdasarkan updated_at terbaru (descending).
        
        LAB 12 SOAL 5: Detail endpoint (retrieve) dapat mengakses laporan DRAFT milik sendiri
        """
        user = self.request.user
        queryset = Report.objects.all().order_by('-updated_at')
        
        # Membaca parameter tab dari URL query parameter
        tab = self.request.query_params.get('tab', None)
        
        if tab == 'my_reports':
            # Filter: Hanya laporan milik user yang login
            queryset = queryset.filter(reporter=user)
        elif tab == 'feed':
            # Filter: Laporan dari warga lain (BUKAN milik user) yang statusnya BUKAN DRAFT
            queryset = queryset.filter(
                ~Q(reporter=user) & ~Q(status='DRAFT') | Q(status='DRAFT', reporter=user)
            )
        else:
            # LAB 12 SOAL 5: Default untuk detail/update endpoint (retrieve dan update)
            # User bisa akses laporan miliknya (termasuk DRAFT) atau laporan public
            if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
                # Detail/Edit endpoint: user bisa akses laporan sendiri atau laporan public (non-DRAFT)
                queryset = queryset.filter(
                    Q(reporter=user) | ~Q(status='DRAFT')
                )
            else:
                # List endpoint default: exclude DRAFT (public feed)
                queryset = queryset.exclude(status='DRAFT')
        
        return queryset

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


# LAB 12: User Registration Endpoint
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    """
    Endpoint untuk mendaftarkan pengguna baru.
    
    Request body:
    {
        "username": "asepiet",
        "email": "asepiet@gmail.com",
        "password": "password123",
        "password_confirm": "password123"
    }
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Pendaftaran berhasil! Silahkan login dengan akun anda.',
            'user': {
                'username': serializer.validated_data['username'],
                'email': serializer.validated_data['email']
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)