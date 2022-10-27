from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, PetSerializer

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


from .models import User, Pet



# Create your views here.
def home(request):
    return HttpResponse('Pet Pal Home Page')

# user sign up 
def signup(request):
    if request.user.is_authenticated:
        # redirect to home page
        return redirect("/")

    if request.method == "POST":
        # create user form has been filled out
        form = UserCreationForm(request.POST)
        # save the form and redirect user to home
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get ("password1")
            user = authenticate(username=username, password=password)
            login (request, user)
        else:
            # return to sign up page THIS ROUTE NEEDS TO BE UPDATED ??? redirect
            return redirect (request, "/" , {"form":form})
    else:
        form = UserCreationForm()
        # return to sign up page THIS ROUTE NEEDS TO BE UPDATED
        # should this be a render
        return redirect (request, "/",{"form": form})

# user login
def signin(request):
    if request.user.is_authenticated:
        # need route for user homepage
        return redirect (request, "user/")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST(["password"])
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            form = AuthenticationForm(request.POST)
            return redirect (request, "/", {'form': form})

    else:
        form = AuthenticationForm()
        return redirect(request, "/", {'form': form})

# user sign out
def signout(request):
    logout(request)
    return redirect('/')

#  ****** PET FUNCTIONS
def pet(request):
    pet = Pet.objects.all()
    return (request, "pet/", {"pet":pet})
# add new pet
def pet_create(request):
    if request.metod == "POST":
        form = request.POST
        if form.is_valid():
            pet = PetSerializer.save()
            return redirect("pet/")
        else: 
            form = PetSerializer
            context = {"form": form, "header":"Add new pet"}
        return (request, "pet/", context)

# edit pet
      






class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class PetView(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    queryset = Pet.objects.all()