from rest_framework import serializers
from .models import Appointments, Health, Pet, User, Daily
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

def validate_password(self, value: str) -> str:
    """
    Hash value passed by user.
    :param value: password of a user
    :return: a hashed version of the password
    """
    return make_password(value)

User = get_user_model()

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = "__all__"
        # fields = ('id', 'name', 'breed', 'date_of_birth', 'nickname', 'catchphrase','user')

class UserSerializer(serializers.ModelSerializer):
    pets =PetSerializer(many=True, required =False)
    def validate_password(self, value: str) -> str:
        return make_password(value)
    class Meta:
        model = User
        fields = "__all__"

class HealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Health
        fields = "__all__"
        # fields = ("id", "visit_date", "visit_type", "pet_weight","shots", "medicine", "other","tx_plan", "pet")

class DailySerializer(serializers.ModelSerializer):
    class Meta:
        model = Daily
        fields = "__all__"
        # fields = ("id","food_schedule", "walk_schedule", "potty_trips", "medicine_schedule", "pet")

class AppointmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = "__all__"
        # fields = ("id", "grooming", "play_date", "cuddles", "pet")