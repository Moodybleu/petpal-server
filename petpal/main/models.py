from multiprocessing.managers import BaseManager
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# User Model


class UserManager(BaseManager):
    def _create_user(self, email, password, username, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password must be provided")
        user = self.model(
            email = self.normalize_email(email),
            username = username
            **extra_fields
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # abstract base user has password, last_login, is active by default
    
    username = models.CharField(unique=True, max_length =250)
    email =models.EmailField(db_index=True, unique=True, max_length = 250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"



class Pet(models.Model):
    name = models.CharField(max_length=100) 
    breed = models.CharField(max_length=100) 
    date_of_birth = models.DateField(null=True)
    nickname = models.CharField(max_length=100) 
    catchphrase = models.CharField(max_length=250) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Pet_Diary(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    # will need FK from health, daily, appts

class Health(models.Model):
    visit_date = models.DateField(null=True)
    visit_type = models.CharField(max_length=250)
    

class Daily(models.Model):
    pass

class Appointments(models.Model):
    pass

    def __str__(self):
        return self.pet