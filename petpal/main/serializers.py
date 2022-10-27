from rest_framework import serializers
from .models import Appointments, Health, Pet, User, Daily
from django.contrib.auth.hashers import make_password

# function to hash password
def validate_password(self, value: str) -> str:
    '''
    hashed value passed by user

    :paramvalue: user password
    :return: hashed pw
    '''
    return make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email','password')

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ('id', 'name', 'breed', 'date_of_birth', 'nickname', 'catchphrase','user')

class HealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Health
        fields = ("id", "visit_date", "visit_type", "pet_weight","shots", "medicine", "other","tx_plan", "pet")

class DailySerializer(serializers.ModelSerializer):
    class Meta:
        model = Daily
        fields = ("id","food_schedule", "walk_schedule", "potty_trips", "medicine_schedule", "pet")

class AppointmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = ("id", "grooming", "play_date", "cuddles", "pet")