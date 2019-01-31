from django.db import models
from django.contrib.auth.models import User

class Ride(models.Model):
    """Ride model"""
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    destination = models.CharField(max_length=1023)
    required_arrival_time = models.DateTimeField()
    number_of_passengers_from_onwer = models.IntegerField()
    number_of_passengers_from_sharers = models.IntegerField(default=0)
    requested_vehicle_type = models.CharField(max_length=255, blank=True)
    special_reqeust = models.TextField(blank=True)
    ride_status = models.CharField(max_length=255, default='open')
    can_be_shared = models.BooleanField(default=False)
    ride_sharers = models.ManyToManyField(User, related_name='ride_sharers')
    user_status = models.CharField(max_length=255, default='free')

    def __str__(self):
        return f'{self.onwer.first_name} {self.owner.last_name}'


