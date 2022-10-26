from enum import unique
from django.db import models


# User Model
class User(models.Model):
    name = models.CharField(max_length=50) 
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50) 

    def __str__(self):
        return self.name

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