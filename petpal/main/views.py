from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions
from django.http import HttpResponse

from .serializers import UserSerializer, PetSerializer

from .models import User, Pet



# Create your views here.
def home(request):
    return HttpResponse('Pet Pal Home Page')
def user(request):
    user = User.objects.all()
    return render (request, "user.html",{})
def pet(request):
    pet = Pet.objects.all()
    return render (request, "", {})

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class PetView(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    queryset = Pet.objects.all()