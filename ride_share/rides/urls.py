from django.urls import path

from . import views


urlpatterns = [
    path('rides', views.rides, name='rides'),
    path('<int:ride_id>', views.ride, name='ride'),
    path('search', views.search, name='search_ride'),
    path('create', views.create, name='create_ride'),
    path('edit/<int:ride_id>', views.edit, name='edit_ride'),
]
