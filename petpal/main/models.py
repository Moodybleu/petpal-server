
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# User Model


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
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
    
    def create_superuser(self, username, email, password, **extra_fields):
        if password is None:
          raise TypeError('Superusers must have a password.')
        if email is None:
            raise TypeError('Superusers must have an email.')
        if username is None:
            raise TypeError('Superusers must have an username.') 

        user = self.create_user(
            username = username,
            email =self.normalize_email,
            password = password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(unique=True, max_length =250)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    def __str__(self):
        return self.username



  

    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)
    #     extra_fields.setdefault('is_active', True)
    #     user = self.create_user(email, username, password, **extra_fields)
    #     user.save()
    #     return user

    # def create_user(self, username, email, password, **extra_fields):
    #     # return self.user
    #     return self.create_user(username, email, password, **extra_fields)

# class User(AbstractBaseUser, PermissionsMixin):
#     # abstract base user has password, last_login, is active by default
    
#     username = models.CharField(unique=True, max_length =250)
#     email =models.EmailField(db_index=True, unique=True, max_length = 250)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
  




class Pet(models.Model):
    name = models.CharField(max_length=100) 
    breed = models.CharField(max_length=100) 
    date_of_birth = models.DateField(null=True)
    nickname = models.CharField(max_length=100) 
    catchphrase = models.CharField(max_length=250) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Health(models.Model):
    visit_date = models.DateField(null=True)
    visit_type = models.CharField(max_length=250,blank=True, null=True)
    pet_weight = models.CharField(max_length=25, blank=True, null=True)
    shots = models.CharField(max_length= 500,blank=True, null=True)
    medicine = models.CharField(max_length=500, blank=True, null=True)
    other =models.TextField(blank=True, null=True)
    tx_plan = models.TextField(blank=True, null=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

class Daily(models.Model):
    food_schedule = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    walk_schedule = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    potty_trips = models.TimeField(auto_now =False, auto_now_add=False, blank=True, null=True)
    medicine_schedule = models.TimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Appointments(models.Model):
    grooming =  models.DateField(null=True, blank=True)
    play_date =  models.DateField(null=True,blank=True)
    cuddles =  models.DateField(null=True,blank=True)

    def __str__(self):
        return self.name

   
class Pet_Diary(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, blank=True, null=True)
    health = models.ForeignKey(Health, on_delete=models.CASCADE, blank=True, null=True)
    daily = models.ForeignKey(Daily, on_delete = models.CASCADE,blank=True, null=True)
    appointments = models.ForeignKey(Appointments, on_delete = models.CASCADE)
