from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Report


User = get_user_model()


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.SerializerMethodField()
    reporter_name = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id', 'title', 'category', 'description', 'location', 'reporter',
            'reporter_name', 'is_owner', 'status', 'created_at', 'updated_at',
        ]
        read_only_fields = ['reporter', 'reporter_name', 'is_owner', 'created_at', 'updated_at']

    def get_reporter(self, obj):
        return "Warga Anonim"

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return bool(request and request.user.is_authenticated and obj.reporter == request.user)

    def get_reporter_name(self, obj):
        if self.get_is_owner(obj) and obj.reporter:
            return obj.reporter.username
        return "Warga Anonim"

    def validate_status(self, value):
        request = self.context.get('request')

        if request:
            is_admin = request.user.is_staff or getattr(request.user, 'is_admin', False)
            is_create = self.instance is None

            if is_admin:
                if self.instance and not self.instance.can_move_to_status(value):
                    raise serializers.ValidationError("Status tidak boleh mundur")

                return value

            if is_create and value in ['DRAFT', 'REPORTED']:
                return value

            if self.instance and self.instance.status == 'DRAFT' and value in ['DRAFT', 'REPORTED']:
                return value

            raise serializers.ValidationError("Citizen tidak boleh mengubah status")

        return value


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Password tidak cocok!")

        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("Username sudah digunakan!")

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email sudah terdaftar!")

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
