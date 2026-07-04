from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'register.html', {
            'title': 'Register',
            'form_action': '/auth/register/',
            'success': False,
            'message': '',
            'errors': {},
        })

    def post(self, request):
        payload = request.data if hasattr(request, 'data') else request.POST
        serializer = RegisterSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()

            if request.content_type and 'application/json' in request.content_type:
                return Response(
                    {
                        'message': 'User berhasil didaftarkan sebagai Citizen.',
                        'user': serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )

            return render(request, 'register.html', {
                'title': 'Register',
                'form_action': '/auth/register/',
                'success': True,
                'message': 'User berhasil didaftarkan sebagai Citizen.',
                'errors': {},
            })

        if request.content_type and 'application/json' in request.content_type:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return render(request, 'register.html', {
            'title': 'Register',
            'form_action': '/auth/register/',
            'success': False,
            'message': 'Registrasi gagal. Periksa kembali input Anda.',
            'errors': serializer.errors,
        })