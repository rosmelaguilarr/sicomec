from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from .models import Driver, Vehicle, FuelTap, Ballot
from .forms import DriverForm, VehicleForm, FuelTapForm, BallotForm
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DriverSerializer, VehicleSerializer

# from django.core.paginator import Paginator
# import os
# from django.http import HttpResponse, Http404
# import mimetypes

# from datetime import datetime
# import pytz
# from django.utils import timezone
# import locale

# from django.template.loader import render_to_string
# from weasyprint import HTML

# from django.db.models import DateField
# from django.db.models.functions import Cast

# ************************************ GENERAL VIEWS ************************************

# HOME ---------------------------------------------------------------->
def home_view(request):
    return render(request, 'index.html')

# LOGIN --------------------------------------------------------------->
def login_view(request):
    if request.user.is_authenticated:
        return redirect('sicomec:home')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('sicomec:home')
            else:
                form.add_error(None, 'Usuario o contraseña incorrecto')
    else:
        form = AuthenticationForm(
            initial={'username': request.POST.get('username', '')})

    return render(request, 'login.html', {'form': form})

# LOGOUT --------------------------------------------------------------->
@login_required
def logout_view(request):
    logout(request)
    return redirect('sicomec:home')



# ************************************ DRIVER VIEWS ************************************

# CREATE --------------------------------------------------------------->
@login_required
def driver_create_view(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, '¡Registro exitoso!')
            return redirect('sicomec:driver_list')  
    else:
        form = DriverForm()
    
    return render(request, 'drivers/driver_create.html', {'form': form})

# UPDATE ----------------------------------------------------------------->
@login_required
def driver_update_view(request, id):
    driver = get_object_or_404(Driver, pk=id)
    query = request.GET.get('q', '')

    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Actualización exitosa!')
            return redirect(f"{reverse('sicomec:driver_list')}?q={query}")
    else:
        formatted_expiration = driver.expiration.strftime('%Y-%m-%d')
        form = DriverForm(instance=driver, initial={'expiration': formatted_expiration})

    return render(request, 'drivers/driver_update.html', {'form': form, 'query': query})

# LIST ------------------------------------------------------------------->
@login_required
def driver_list_view(request):
    query = request.GET.get('q', '').strip()
    search_performed = False
    results = []
    message = ""
    driver_count = 0

    if query:
        search_performed = True
        drivers = Driver.objects.filter(
            Q(dni__icontains=query) |
            Q(name__icontains=query) |
            Q(last_name__icontains=query)
        )
        results = drivers

        if results.exists():
            driver_count = results.count()
        else:
            message = "No se encontraron conductores con esos criterios"

    return render(request, 'drivers/driver_list.html', 
                {
                    'drivers': results,
                    'query': query,
                    'search_performed':search_performed,
                    'driver_count': driver_count,
                    'message': message,
                })




# SEARCH BY DNI ------------------------------------------------------------------>
@api_view(['GET'])
def search_driver_by_dni(request):
    dni = request.GET.get('dni')
    driver = Driver.objects.filter(dni=dni).first()
    
    if driver:
        serializer = DriverSerializer(driver)
        return Response(serializer.data)
    else:
        return Response({'error': 'Driver not found'}, status=404)

# DELETE ------------------------------------------------------------------>
@login_required
def driver_delete_view(request, id):
    driver = get_object_or_404(Driver, pk=id)
    driver.delete()
    messages.success(request, '¡Registro eliminado!')
    return redirect('sicomec:driver_list')  



# ************************************ VEHICLE VIEWS ************************************

# CREATE --------------------------------------------------------------->
@login_required
def vehicle_create_view(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, '¡Registro exitoso!')
            return redirect('sicomec:vehicle_list')  
    else:
        form = VehicleForm()
    
    return render(request, 'vehicles/vehicle_create.html', {'form': form})

# UPDATE ----------------------------------------------------------------->
@login_required
def vehicle_update_view(request, id):
    vehicle = get_object_or_404(Vehicle, pk=id)
    query = request.GET.get('q', '')

    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Actualización exitosa!')
            return redirect(f"{reverse('sicomec:vehicle_list')}?q={query}")
    else:
        form = VehicleForm(instance=vehicle, initial={
                            'production': vehicle.production.strftime('%Y-%m-%d'),
                            'soat': vehicle.soat.strftime('%Y-%m-%d'),
                            'citv': vehicle.citv.strftime('%Y-%m-%d'),
                            })

    return render(request, 'vehicles/vehicle_update.html', {'form': form, 'query': query,})

# LIST ------------------------------------------------------------------->
@login_required
def vehicle_list_view(request):
    query = request.GET.get('q', '').strip()
    search_performed = False
    results = []
    message = ""
    vehicle_count = 0

    if query:
        search_performed = True
        vehicles = Vehicle.objects.filter(
            Q(plate__icontains=query) |
            Q(brand__icontains=query)
        )
        results = vehicles

        if results.exists():
            vehicle_count = results.count()
        else:
            message = "No se encontraron vehículos con esos criterios"

    return render(request, 'vehicles/vehicle_list.html', 
                {
                    'vehicles': results,
                    'query': query,
                    'search_performed':search_performed,
                    'vehicle_count': vehicle_count,
                    'message': message,
                })

# SEARCH BY PLATE ------------------------------------------------------------------>
@api_view(['GET'])
def search_vehicle_by_plate(request):
    plate = request.GET.get('plate')
    vehicle = Vehicle.objects.filter(plate=plate).first()
    
    if vehicle:
        serializer = VehicleSerializer(vehicle)
        return Response(serializer.data)
    else:
        return Response({'error': 'Vehicle not found'}, status=404)

# DELETE ------------------------------------------------------------------>
@login_required
def vehicle_delete_view(request, id):
    vehicle = get_object_or_404(Vehicle, pk=id)
    vehicle.delete()
    messages.success(request, '¡Registro eliminado!')
    return redirect('sicomec:vehicle_list')  



# ************************************ FUELTAP VIEWS ************************************

# CREATE --------------------------------------------------------------->
@login_required
def fueltap_create_view(request):
    if request.method == 'POST':
        form = FuelTapForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, '¡Registro exitoso!')
            return redirect('sicomec:fueltap_list')  
    else:
        form = FuelTapForm()
    
    return render(request, 'fueltaps/fueltap_create.html', {'form': form})

# UPDATE ----------------------------------------------------------------->
@login_required
def fueltap_update_view(request, id):
    fueltap = get_object_or_404(FuelTap, pk=id)
    query = request.GET.get('q', '')

    if request.method == 'POST':
        form = FuelTapForm(request.POST, instance=fueltap)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Actualización exitosa!')
            return redirect(f"{reverse('sicomec:fueltap_list')}?q={query}")
    else:
        form = FuelTapForm(instance=fueltap)

    return render(request, 'fueltaps/fueltap_update.html', {'form': form, 'query': query,})

# LIST ------------------------------------------------------------------->
@login_required
def fueltap_list_view(request):
    query = request.GET.get('q', '').strip()
    search_performed = False
    results = []
    message = ""
    fueltap_count = 0

    if query:
        search_performed = True
        fueltaps = FuelTap.objects.filter(
            Q(ruc__icontains=query) |
            Q(business_name__icontains=query)
        )
        results = fueltaps

        if results.exists():
            fueltap_count = results.count()
        else:
            message = "No se encontraron grifos con esos criterios"

    return render(request, 'fueltaps/fueltap_list.html', 
                {
                    'fueltaps': results,
                    'query': query,
                    'search_performed':search_performed,
                    'fueltap_count': fueltap_count,
                    'message': message,
                })

# DELETE ------------------------------------------------------------------>
@login_required
def fueltap_delete_view(request, id):
    fueltap = get_object_or_404(FuelTap, pk=id)
    fueltap.delete()
    messages.success(request, '¡Registro eliminado!')
    return redirect('sicomec:fueltap_list')  



# ************************************ BALLOT VIEWS ************************************

# CREATE --------------------------------------------------------------->
@login_required
def ballot_create_view(request):
    if request.method == 'POST':
        form = BallotForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, '¡Registro exitoso!')
            return redirect('sicomec:ballot_list')  
    else:
        form = BallotForm()
    
    return render(request, 'ballots/ballot_create.html', {'form': form})

# # UPDATE ----------------------------------------------------------------->
@login_required
def ballot_update_view(request, id):
    ballot = get_object_or_404(Ballot, pk=id)
    query = request.GET.get('q', '')

    if request.method == 'POST':
        form = BallotForm(request.POST, instance=ballot)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Actualización exitosa!')
            return redirect(f"{reverse('sicomec:ballot_list')}?q={query}")
    else:
        form = BallotForm(instance=ballot, initial={
                            'exit_date': ballot.exit_date.strftime('%Y-%m-%d'),
                            })

    return render(request, 'ballots/ballot_update.html', {'form': form, 'query': query,})

# # LIST ------------------------------------------------------------------->
@login_required
def ballot_list_view(request):
    query = request.GET.get('q', '').strip()
    search_performed = False
    results = []
    message = ""
    ballot_count = 0

    if query:
        search_performed = True
        ballots = Ballot.objects.filter(
            Q(code__icontains=query) |
            Q(vehicle_plate__icontains=query)
        )
        results = ballots

        if results.exists():
            ballot_count = results.count()
        else:
            message = "No se encontraron grifos con esos criterios"

    return render(request, 'ballots/ballot_list.html', 
                {
                    'ballots': results,
                    'query': query,
                    'search_performed':search_performed,
                    'ballot_count': ballot_count,
                    'message': message,
                })

# # DELETE ------------------------------------------------------------------>
@login_required
def ballot_delete_view(request, id):
    ballot = get_object_or_404(Ballot, pk=id)
    ballot.delete()
    messages.success(request, '¡Registro eliminado!')
    return redirect('sicomec:ballot_list')  



# ************************************ ERROR VIEWS ************************************

def error_404(request, exception):
    return render(request, '404.html', {})

def error_403(request, exception):
    return render(request, '403.html', status=403)
