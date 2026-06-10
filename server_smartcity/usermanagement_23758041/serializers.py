from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # Menyembunyikan password agar tidak memantul kembali berupa teks biasa saat respons sukses
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # Sesuaikan field ini dengan field yang ada pada Custom User Model Anda di Lab 6
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        """
        Meng-override method create agar password di-hash secara aman 
        dan memastikan user yang mendaftar otomatis memiliki role Citizen (bukan admin/staff).
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_staff=False,  # Memastikan bukan Admin/Staff
            is_superuser=False
        )
        return user