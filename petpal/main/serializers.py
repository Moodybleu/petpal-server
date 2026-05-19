from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import Appointments, Daily, Health, Pet, User


class PetSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = [
            'id',
            'name',
            'breed',
            'age',
            'nickname',
            'catchphrase',
            'photo',
            'photo_url',
        ]
        extra_kwargs = {
            'photo': {'write_only': True, 'required': False, 'allow_null': True},
        }

    def get_photo_url(self, obj):
        if not obj.photo:
            return None
        try:
            url = obj.photo.url
        except (ValueError, AttributeError):
            return None
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(url)
        return url


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'username']
        extra_kwargs = {
            'name': {'required': False, 'allow_blank': True},
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        username = attrs.pop('username', None)
        if username and not attrs.get('name'):
            attrs['name'] = username
        if not attrs.get('name'):
            raise serializers.ValidationError({'name': 'Username is required.'})
        return attrs

    def validate_email(self, value: str) -> str:
        email = value.strip()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                'An account with this email already exists. Log in or use Reset password.'
            )
        return email

    def validate_password(self, value: str) -> str:
        return make_password(value)


class HealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Health
        fields = '__all__'


class DailySerializer(serializers.ModelSerializer):
    class Meta:
        model = Daily
        fields = '__all__'


class AppointmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = '__all__'
