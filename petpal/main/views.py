from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions
from django.http import HttpResponse

from .serializers import UserSerializer, PetSerializer, HealthSerializer, DailySerializer, AppointmentsSerializer

from .models import Appointments, User, Pet, Health, Daily, Appointments
from main import serializers



# Create your views here.
def home(request):
    return HttpResponse('Pet Pal Home Page')

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class PetView(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    queryset = Pet.objects.all()

class HealthView(viewsets.ModelViewSet):
    serializer_class = HealthSerializer
    queryset = Health.objects.all()

class DailyView(viewsets.ModelViewSet):
    serializer_class = DailySerializer
    queryset = Daily.objects.all()

class AppointmentsView(viewsets.ModelViewSet):
    serializer_class = AppointmentsSerializer
    queryset = Appointments.objects.all()






