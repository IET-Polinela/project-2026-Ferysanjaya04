from django.db.models import Q
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema 
from .models import Report
from .serializers import ReportSerializer

#@extend_schema_view(
 #   list=extend_schema(exclude=True),
 #  retrieve=extend_schema(exclude=True),
 #  create=extend_schema(exclude=True),
 #   update=extend_schema(exclude=True),
 #  partial_update=extend_schema(exclude=True),
 #   destroy=extend_schema(exclude=True),
#)

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def is_admin_user(self, user):
        return user.is_staff or getattr(user, 'is_admin', False)

    def get_queryset(self):
        user = self.request.user
        tab = self.request.query_params.get('tab')

        if self.is_admin_user(user):
            return Report.objects.all().order_by('-updated_at')

        if tab == 'feed':
            return Report.objects.exclude(status='DRAFT').order_by('-updated_at')

        if tab == 'my_reports':
            return Report.objects.filter(reporter=user).order_by('-updated_at')

        return Report.objects.filter(
            Q(reporter=user) | ~Q(status='DRAFT')
        ).order_by('-updated_at')

    def perform_create(self, serializer):
        if self.is_admin_user(self.request.user):
            raise permissions.PermissionDenied("Admin tidak boleh membuat laporan")

        serializer.save(reporter=self.request.user)

    def create(self, request, *args, **kwargs):
        if self.is_admin_user(request.user):
            return Response(
                {'error': 'Admin tidak boleh membuat laporan'},
                status=403
            )

        report_status = request.data.get('status', 'DRAFT')
        if report_status not in ['DRAFT', 'REPORTED']:
            return Response(
                {'status': ['Citizen hanya boleh membuat laporan DRAFT atau REPORTED']},
                status=400
            )

        data = {
            'title': request.data.get('title', ''),
            'category': request.data.get('category', ''),
            'description': request.data.get('description', ''),
            'location': request.data.get('location', ''),
            'status': report_status,
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reporter=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if self.is_admin_user(request.user):
            allowed_fields = {'status'}
            sent_fields = set(request.data.keys())

            if not sent_fields.issubset(allowed_fields):
                return Response(
                    {'error': 'Admin hanya boleh mengubah status laporan'},
                    status=403
                )

            serializer = self.get_serializer(
                instance,
                data={'status': request.data.get('status')},
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        if instance.reporter != request.user:
            return Response(
                {'error': 'Tidak diizinkan'},
                status=403
            )

        if instance.status != 'DRAFT':
            return Response(
                {'error': 'Laporan yang sudah diajukan hanya bisa dilihat oleh citizen'},
                status=403
            )

        if 'status' in request.data and request.data.get('status') not in ['DRAFT', 'REPORTED']:
            return Response(
                {'error': 'Citizen tidak boleh mengubah status'},
                status=403
            )

        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if self.is_admin_user(request.user):
            return Response(
                {'error': 'Admin tidak boleh menghapus laporan'},
                status=403
            )

        if instance.reporter != request.user:
            return Response(
                {'error': 'Tidak diizinkan'},
                status=403
            )

        return super().destroy(request, *args, **kwargs)
