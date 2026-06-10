from rest_framework import serializers
from .models import Report
from django.contrib.auth.models import User


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = '__all__'

    def get_reporter(self, obj):
        return "Warga Anonim"


# LAB 12: User Registration Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, attrs):
        # Validasi password match
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Password tidak cocok!")
        
        # Validasi username tidak ada yang sama
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("Username sudah digunakan!")
        
        # Validasi email tidak ada yang sama
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email sudah terdaftar!")
        
        return attrs

    def create(self, validated_data):
        # Hapus field password_confirm sebelum create
        validated_data.pop('password_confirm', None)
        
        # Create user dengan password hash
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user