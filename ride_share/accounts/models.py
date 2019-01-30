from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class DriverProfile(models.Model):
    """Driver's Profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    vehicleNumber = models.CharField(max_length=20)
    specialVehicleInfo = models.TextField(blank=True)
    is_driver = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_driver_profile(sender, instance, created, **kwargs):
    if created:
        DriverProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_driver_profile(sender, instance, **kwargs):
    instance.driverProfile.save()



