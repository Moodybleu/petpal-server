from ssl import DefaultVerifyPaths
from django.contrib import admin

from .models import Appointments, Daily, Pet_Diary, User, Health
from .models import Pet

# Register your models here.
admin.site.register(User)
admin.site.register(Pet)
admin.site.register(Pet_Diary)
admin.site.register(Health)
admin.site.register(Daily)
admin.site.register(Appointments)