from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from .models import Driver, Vehicle, FuelTap, Ballot
from .forms import DriverForm, VehicleForm, FuelTapForm, BallotForm
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DriverSerializer, VehicleSerializer
from django.utils import timezone
import pytz

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from babel.dates import format_datetime


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
        results = Driver.objects.filter(
            Q(dni__icontains=query) |
            Q(name__icontains=query) |
            Q(last_name__icontains=query)
        )
        if results.exists():
            driver_count = results.count()
        else:
            message = "No se encontraron conductores con esos criterios"
    else:
        results = Driver.objects.all()
        driver_count = results.count()

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
    try:
        driver = Driver.objects.get(dni=dni)
        if driver.available:
            serializer = DriverSerializer(driver)
            return Response(serializer.data)
        else:
            return Response({'error': 'Conductor No Disponible'}, status=404)
    except Driver.DoesNotExist:
        return Response({'error': 'Conductor No Existe'}, status=404)

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
        results = Vehicle.objects.filter(
            Q(plate__icontains=query) |
            Q(brand__icontains=query)
        )
        if results.exists():
            vehicle_count = results.count()
        else:
            message = "No se encontraron vehículos con esos criterios"
    else:
        results = Vehicle.objects.all()
        vehicle_count = results.count()

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
    try:
        vehicle = Vehicle.objects.get(plate=plate)
        if vehicle.available:
            serializer = VehicleSerializer(vehicle)
            return Response(serializer.data)
        else:
            return Response({'error': 'Vehículo No Disponible'}, status=404)
    except Vehicle.DoesNotExist:
        return Response({'error': 'Vehículo No Existe'}, status=404)

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
        results = FuelTap.objects.filter(
            Q(ruc__icontains=query) |
            Q(business_name__icontains=query)
        )
        if results.exists():
            fueltap_count = results.count()
        else:
            message = "No se encontraron grifos con esos criterios"
    else:
        results = FuelTap.objects.all()
        fueltap_count = results.count()

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
            ballot = form.save(commit=False)
            ballot.user = request.user

            driver_dni = request.POST.get('driver_dni')
            vehicle_plate = request.POST.get('vehicle_plate')

            if driver_dni:
                ballot.driver_dni = driver_dni

                driver = Driver.objects.get(dni=driver_dni)
                driver.available = False
                driver.save()
            
            if vehicle_plate:
                    vehicle = Vehicle.objects.get(plate=vehicle_plate)
                    vehicle.available = False
                    vehicle.save()

            ballot.save()
            messages.success(request, '¡Registro exitoso!')
            return redirect('sicomec:ballot_list_scheduled')
    else:
        form = BallotForm()

    return render(request, 'ballots/ballot_create.html', {'form': form})

# UPDATE ----------------------------------------------------------------->
@login_required
def ballot_update_view(request, id):
    ballot = get_object_or_404(Ballot, pk=id)
    query = request.GET.get('q', '')

    if request.method == 'POST':
        form = BallotForm(request.POST, instance=ballot)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Actualización exitosa!')
            return redirect(f"{reverse('sicomec:ballot_list_scheduled')}?q={query}")
    else:
        form = BallotForm(instance=ballot, initial={
                            'exit_date': ballot.exit_date.strftime('%Y-%m-%d'),
                            })

    return render(request, 'ballots/ballot_update.html', {'form': form, 'query': query,})

# LIST SCHEDULED------------------------------------------------------------------->
@login_required
def ballot_list_scheduled_view(request):
    query = request.GET.get('q', '').strip()
    search_performed = False
    results = []
    message = ""
    ballot_count = 0

    if query:
        search_performed = True
        results = Ballot.objects.filter(
            (Q(code__icontains=query) | Q(vehicle_plate__icontains=query)) &
            Q(return_date__isnull=True) &
            Q(return_time__isnull=True)
        )
        
        if results.exists():
            ballot_count = results.count()
        else:
            message = "No se encontraron papeletas con esos criterios."
    else:
        results = Ballot.objects.filter(
            return_date__isnull=True,
            return_time__isnull=True
        )
        ballot_count = results.count()

    return render(request, 'ballots/ballot_list_scheduled.html', 
                {
                    'ballots': results,
                    'query': query,
                    'search_performed': search_performed,
                    'ballot_count': ballot_count,
                    'message': message,
                })

# LIST COMPLETE------------------------------------------------------------------->
@login_required
def ballot_list_complete_view(request):
    query = request.GET.get('q', '').strip()
    search_performed = False
    results = []
    message = ""
    ballot_count = 0

    if query:
        search_performed = True
        results = Ballot.objects.filter(
            (Q(code__icontains=query) | Q(vehicle_plate__icontains=query)) &
            Q(return_date__isnull=False) &
            Q(return_time__isnull=False)
        )
        
        if results.exists():
            ballot_count = results.count()
        else:
            message = "No se encontraron papeletas con esos criterios."
    else:
        results = Ballot.objects.filter(
            return_date__isnull=False,
            return_time__isnull=False
        )
        ballot_count = results.count()

    return render(request, 'ballots/ballot_list_complete.html', 
                {
                    'ballots': results,
                    'query': query,
                    'search_performed': search_performed,
                    'ballot_count': ballot_count,
                    'message': message,
                })

# MARK RETURN------------------------------------------------------------------->
@login_required
def ballot_mark_return_view(request):
    query = request.GET.get('q', '').strip()
    search_performed = False
    results = []
    message = ""
    ballot_count = 0

    if query:
        search_performed = True
        results = Ballot.objects.filter(
            Q(code__exact=query) &
            Q(return_date__isnull=True) &
            Q(return_time__isnull=True)
        )
        
        if results.exists():
            ballot_count = results.count()
        else:
            message = "Código de papeleta no encontrada"

    return render(request, 'ballots/ballot_mark_return.html', 
                {
                    'ballots': results,
                    'query': query,
                    'search_performed': search_performed,
                    'ballot_count': ballot_count,
                    'message': message,
                })

# UPDATE RETURN_DATE AND RETURN_TIME------------------------------------------------------------------->
@login_required
def update_return_datetime(request, id):
    ballot = get_object_or_404(Ballot, id=id)
    driver_dni = ballot.driver_dni
    vehicle_plate = ballot.vehicle_plate
    query = request.GET.get('q', '')

    lima_tz = pytz.timezone('America/Lima')
    current_time = timezone.now().astimezone(lima_tz)
    ballot.return_date = current_time.date()
    ballot.return_time = current_time.time()

    if driver_dni:
            driver = Driver.objects.get(dni=driver_dni)
            driver.available = True
            driver.save()

    if vehicle_plate:
            vehicle = Vehicle.objects.get(plate=vehicle_plate)
            vehicle.available = True
            vehicle.save()

    ballot.save()
    messages.success(request, '¡Retorno marcado!')
    return redirect(f"{reverse('sicomec:ballot_mark_return')}?q={query}")

# GENEREATE PDF ------------------------------------------------------------------>
def generate_ballot_pdf(request, id):
    ballot = get_object_or_404(Ballot, pk=id)

    base_url = 'file:///C:/sicomec/'
    current_date = timezone.localtime(timezone.now(), timezone=pytz.timezone('America/Lima'))
    date_print = format_datetime(current_date, format="d'/'MM'/'yyyy HH:mm", locale='es')


    data = {
        'date': date_print,
        'base_url':base_url,
        'ballot': ballot,
        'current_date': current_date,
    }

    # Renderiza la plantilla con los datos
    html_string = render_to_string('ballots/ballot_template_pdf.html', data)

    filename = current_date.strftime('%d-%m-%Y %H.%M') + "_reporte.pdf"
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response

# DELETE ------------------------------------------------------------------>
@login_required
def ballot_delete_view(request, id):
    ballot = get_object_or_404(Ballot, pk=id)
    driver_dni = ballot.driver_dni
    vehicle_plate = ballot.vehicle_plate
    
    ballot.delete()
    
    if driver_dni:
            driver = Driver.objects.get(dni=driver_dni)
            driver.available = True
            driver.save()

    if vehicle_plate:
            vehicle = Vehicle.objects.get(plate=vehicle_plate)
            vehicle.available = True
            vehicle.save()
    
    messages.success(request, '¡Registro eliminado!')

    redirect_to = request.GET.get('redirect_to', 'scheduled')
    if redirect_to == 'completed':
        return redirect('sicomec:ballot_list_complete')
    else:
        return redirect('sicomec:ballot_list_scheduled')


# ************************************ ERROR VIEWS ************************************

def error_404(request, exception):
    return render(request, '404.html', {})

def error_403(request, exception):
    return render(request, '403.html', status=403)
