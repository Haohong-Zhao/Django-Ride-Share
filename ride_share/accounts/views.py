from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.http import HttpResponse

from .models import DriverProfile

from .utils import is_email, is_driver, get_driver_profile_by_request

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if is_email(email) is False:
            messages.error(request, 'Wrong formatted email address.')
            return redirect('register')
        elif password != password2:
            messages.error(request, 'Passwords mismatch.')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is being used.')
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('register')
        else: # validation passed
            user = User.objects.create_user(
                username=username, email=email, 
                password=password, first_name=first_name, 
                last_name=last_name
            )
            user.save()
            messages.success(request, 'You are now registered and can login.')
            return redirect('login')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')

        else:
            messages.error(request, 'Invalid credential')
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html')



def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You have successfully logged out.')
        return redirect('index')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def driver_register(request):
    # For post method
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        else:
            vehicle_number = request.POST['vehicle_number']
            special_vehicle_info = request.POST['special_vehicle_info']
            
            driver_profile = get_driver_profile_by_request(request)

            driver_profile.vehicle_number = vehicle_number
            driver_profile.special_vehicle_info = special_vehicle_info
            driver_profile.save(update_fields=[
                'vehicle_number', 'special_vehicle_info'
            ])
            messages.success(request, 'Congratulate on being a driver.')
            return redirect('dashboard')

    # For Get Method
    if not request.user.is_authenticated:
        messages.error(request, 'Log in is required for driver registration.')
        return redirect('login')
    else:
        if is_driver(request):
            messages.error(request, 'You are already a driver.')
            return redirect('dashboard')
        else:
            return render(request, 'accounts/driver_register.html')


def driver_update_info(request):
    # For post method
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        else:
            vehicle_number = request.POST['vehicle_number']
            special_vehicle_info = request.POST['special_vehicle_info']

            driver_profile = get_driver_profile_by_request(request)

            driver_profile.vehicle_number = vehicle_number
            driver_profile.special_vehicle_info = special_vehicle_info
            driver_profile.save(update_fields=[
                'vehicle_number', 'special_vehicle_info'
            ])
            messages.success(request, 'Update driver\'s info successfully.')
            return redirect('dashboard')

    # For Get Method
    if not request.user.is_authenticated:
        messages.error(request, 'Log in is required for driver registration.')
        return redirect('login')
    else:
        if not is_driver(request):
            messages.error(request, 'You are not a driver.')
            return redirect('driver_register')
        else:
            return render(request, 'accounts/driver_update_info.html')
