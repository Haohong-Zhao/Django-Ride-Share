from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from datetime import datetime

from accounts.utils import get_checkbox_input

from .models import Ride


def rides(request):
    """List all rides"""
    # Authentication
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    
    user = User.objects.get(id=request.user.id)
    rides_as_owner = user.rides_as_owner.all().order_by('id')
    rides_as_driver = user.rides_as_driver.all().order_by('id')
    rides_as_sharer = user.rides_as_sharer.all().order_by('id')

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
    """Create a ride(as owner)"""
    # Authentication
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    # POST
    if request.method == 'POST':
        # get user
        user = User.objects.get(id=request.user.id)
        # get form inputs
        destination = request.POST['destination']
        required_arrival_time_in_text = request.POST['arrival_time']
        passenger_number_from_owner = request.POST['number_of_passengers']
        requested_vehicle_type = request.POST['vehicle_type']
        special_reqeust = request.POST['special_request']
        can_be_shared = get_checkbox_input('can_be_shared', request)
        print('can_be_shared is ', can_be_shared)
        # string to required format(if needed)
        required_arrival_time_in_text = required_arrival_time_in_text.replace('.', '') # Jan. 1, 2019, 12:12 p.m.
        required_arrival_time = datetime.strptime(  # Jan 1, 2019, 12:12 pm
            required_arrival_time_in_text, "%b %d, %Y, %I:%M %p"
        )
        # create object
        Ride.objects.create(
            owner=user,
            destination=destination, required_arrival_time=required_arrival_time,
            passenger_number_from_owner=passenger_number_from_owner,
            can_be_shared=can_be_shared, 
            requested_vehicle_type=requested_vehicle_type, 
            special_reqeust=special_reqeust,
        )
        # send message & return
        messages.success(request, 'You have successfully made a request.')
        return redirect('create_ride')
    # GET
    return render(request, 'rides/create.html')


def edit(request, ride_id):
    """Edit a ride"""
    # Authentication
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    # Identify User's role
    user = User.objects.get(id=request.user.id)
    ride = Ride.objects.get(id=ride_id) # get the ride with ride_id
    user_role = None
    if ride.owner.id == user.id:
        user_role = 'owner'
    elif ride.driver is not None and ride.driver.id == user.id:
        user_role = 'driver'
    elif User.objects.filter(rides_as_sharer__id=ride.id, id=user.id).exists():
        user_role = 'sharer'
    # Not related to this ride
    if user_role is None:
        return HttpResponse(status=404)
    # GET: Display ride information
    if request.method == 'GET':
        context = {
            'ride': ride
        }
        return render(request, 'rides/edit.html', context)
    # POST: Update ride information
    if request.method == 'POST':
        # get form inputs
        destination = request.POST['destination']
        required_arrival_time_in_text = request.POST['arrival_time']
        passenger_number_from_owner = request.POST['number_of_passengers']
        requested_vehicle_type = request.POST['vehicle_type']
        special_reqeust = request.POST['special_request']
        can_be_shared = get_checkbox_input('can_be_shared', request)
        print('can_be_shared is ', can_be_shared)
        # string to required format(if needed)
        # Jan. 1, 2019, 12:12 p.m.
        required_arrival_time_in_text = required_arrival_time_in_text.replace(
            '.', '')
        required_arrival_time = datetime.strptime(  # Jan 1, 2019, 12:12 pm
            required_arrival_time_in_text, "%b %d, %Y, %I:%M %p"
        )
        # Update ride information
        ride.destination = destination
        ride.required_arrival_time = required_arrival_time
        ride.passenger_number_from_owner = passenger_number_from_owner
        ride.can_be_shared = can_be_shared
        ride.requested_vehicle_type = requested_vehicle_type
        ride.special_reqeust = special_reqeust
        ride.save()

        return redirect('rides')
