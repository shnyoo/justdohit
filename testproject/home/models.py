from django.db import models
from django.conf import settings 
from django.contrib.auth.models import User
from django.utils import timezone

class Vehicle(models.Model):
    name = models.CharField(max_length=200)
    passNum = models.IntegerField()
    lat = models.FloatField()
    lon = models.FloatField()
    availableStartDate = models.DateField()
    availableEndDate = models.DateField()

    cur_battery = models.IntegerField()
    max_battery = models.IntegerField()
    
    bedNum = models.IntegerField()
    fridge = models.BooleanField()
    mcwave = models.BooleanField()
    tv = models.BooleanField()
    booked = models.BooleanField()

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Travel(models.Model):
    start = models.CharField(max_length=200)
    dest = models.CharField(max_length=200)

    start_date = models.DateField(default=timezone.now)
    arriv_date = models.DateField()

    start_time = models.TimeField(default=timezone.now)
    arriv_time = models.TimeField()

    travelerNum = models.IntegerField()
    traveler = models.ForeignKey(User, on_delete=models.CASCADE)


class Ride(models.Model):
    start = models.CharField(max_length=200)
    dest = models.CharField(max_length=200)

    start_time = models.DateTimeField(default=timezone.now)
    arriv_time = models.DateTimeField()

    schedule = models.ForeignKey(Travel, on_delete=models.CASCADE, null=True)