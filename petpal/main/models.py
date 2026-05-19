from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Pet(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    catchphrase = models.CharField(max_length=250)
    photo = models.ImageField(upload_to='pets/', blank=True, null=True)

    def __str__(self):
        return self.name


class Health(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='health_records', null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    visit_type = models.CharField(max_length=100, blank=True)
    pet_weight = models.CharField(max_length=50, blank=True)
    shots = models.CharField(max_length=255, blank=True)
    meds = models.CharField(max_length=255, blank=True)
    other = models.TextField(blank=True)
    tx_plan = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'Health #{self.pk}'


class Daily(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='daily_logs', null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    log_type = models.CharField(max_length=50, default='general', blank=True)
    details = models.TextField(blank=True)
    daily_schedule = models.TextField(blank=True)

    def __str__(self):
        return f'Daily #{self.pk}'


class Appointments(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)
    title = models.CharField(max_length=100, default='Appointment', blank=True)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField(null=True, blank=True)
    appointment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Appointment #{self.pk}'
