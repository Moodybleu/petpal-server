from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions
from django.http import HttpResponse

from .serializers import UserSerializer, PetSerializer, HealthSerializer, DailySerializer, AppointmentsSerializer

from .models import Appointments, User, Pet, Health, Daily, Appointments



# Create your views here.
def home(request):
    return HttpResponse('Pet Pal Home Page')
# def user(request):
#     user = User.objects.all()
#     return render (request, "user.html",{})
# def pet(request):
#     pet = Pet.objects.all()
#     return render (request, "", {})

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




# from django.urls import path
# from . import views
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
# from .views import MeView

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('instruments/', views.instruments, name='instruments'),
#     path('students/', views.students, name='students'),
#     path('teachers/', views.teachers, name='teachers'),
#     path('users/', views.users, name='users'),
#     path('reviews/', views.reviews, name='reviews'),
#     path('inquiries/', views.inquiries, name='inquiries'),
#     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('me/', MeView.as_view(), name='me'),
# ]