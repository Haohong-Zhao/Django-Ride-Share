from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User

from .models import Ride


def rides(request):
    """List all rides"""
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    
    user = User.objects.get(id=request.user.id)
    rides_as_owner = user.rides_as_owner.all().order_by('destination')
    rides_as_driver = user.rides_as_driver.all().order_by('destination')
    rides_as_sharer = user.rides_as_sharer.all().order_by('destination')

    context = {
        'rides_as_owner': rides_as_owner,
        'rides_as_driver': rides_as_driver,
        'rides_as_sharer': rides_as_sharer,
    }

    return render(request, 'rides/rides.html', context)


def ride(request, ride_id):
    """Detail page for ride with ride_id"""
    return render(request, 'rides/ride.html')


def search(request):
    """Return search results"""
    return render(request, 'rides/search.html')


def create(request):
    """Create a ride(as onwer)"""
    return render(request, 'rides/create.html')


def edit(request, ride_id):
    """Edit a ride"""
    return render(request, 'rides/edit.html')
