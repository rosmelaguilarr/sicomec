from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from .models import Driver, Vehicle, FuelTap, Ballot, Notification, BuyOrder, FuelOrder
from .forms import DriverForm, VehicleForm, FuelTapForm, BallotForm, BuyOrderForm, FuelOrderForm
from django.contrib import messages
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import datetime
import pytz
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from babel.dates import format_datetime
from django.http import JsonResponse
from django.http import Http404
import re
from django.db import IntegrityError
from django.templatetags.static import static

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
@permission_required('sicoapp.add_driver', raise_exception=True)
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
@permission_required('sicoapp.change_driver', raise_exception=True)
def driver_update_view(request, id):
    driver = get_object_or_404(Driver, pk=id)

    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Actualización exitosa!')
            return redirect('sicomec:driver_list')
    else:
        formatted_expiration = driver.expiration.strftime('%Y-%m-%d')
        form = DriverForm(instance=driver, initial={'expiration': formatted_expiration})

    return render(request, 'drivers/driver_update.html', {'form': form, })

# LIST ------------------------------------------------------------------->
@login_required
@permission_required('sicoapp.view_driver', raise_exception=True)
def driver_list_view(request):
    results = Driver.objects.all()

    return render(request, 'drivers/driver_list.html', 
                {
                    'drivers': results,
                })

# DELETE ------------------------------------------------------------------>
@login_required
@permission_required('sicoapp.delete_driver', raise_exception=True)
def driver_delete_view(request, id):
    driver = get_object_or_404(Driver, pk=id)

    if Ballot.objects.filter(driver=driver.pk).exists():
        messages.warning(request, 'Conductor tiene papeleta asociada')
        return redirect('sicomec:driver_list')  

    if FuelOrder.objects.filter(driver=driver.pk).exists():
        messages.warning(request, 'Conductor tiene orden de compra asociada')
        return redirect('sicomec:driver_list')  
    
    driver.delete()
    messages.success(request, '¡Registro eliminado!')

    return redirect('sicomec:driver_list')  



# ************************************ VEHICLE VIEWS ************************************

# CREATE --------------------------------------------------------------->
@login_required
@permission_required('sicoapp.add_vehicle', raise_exception=True)
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
@permission_required('sicoapp.change_vehicle', raise_exception=True)
def vehicle_update_view(request, id):
    vehicle = get_object_or_404(Vehicle, pk=id)

    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Actualización exitosa!')
            return redirect('sicomec:vehicle_list')
    else:
        form = VehicleForm(instance=vehicle, initial={
                            'soat': vehicle.soat.strftime('%Y-%m-%d') if vehicle.soat else '',
                            'citv': vehicle.citv.strftime('%Y-%m-%d') if vehicle.citv else '',
                            })

    return render(request, 'vehicles/vehicle_update.html', {'form': form,})

# LIST ------------------------------------------------------------------->
@login_required
@permission_required('sicoapp.view_vehicle', raise_exception=True)
def vehicle_list_view(request):
    results = Vehicle.objects.all()

    return render(request, 'vehicles/vehicle_list.html', {'vehicles': results,})

# DELETE ------------------------------------------------------------------>
@login_required
@permission_required('sicoapp.delete_vehicle', raise_exception=True)
def vehicle_delete_view(request, id):
    vehicle = get_object_or_404(Vehicle, pk=id)

    if Ballot.objects.filter(plate=vehicle.id).exists():
        messages.warning(request, 'Vehículo tiene papeleta asociada')
        return redirect('sicomec:vehicle_list')  

    if FuelOrder.objects.filter(plate=vehicle.id).exists():
        messages.warning(request, 'Vehículo tiene órden de compra asociada')
        return redirect('sicomec:vehicle_list')  
    
    vehicle.delete()
    messages.success(request, '¡Registro eliminado!')

    return redirect('sicomec:vehicle_list')  



# ************************************ FUELTAP VIEWS ************************************

# CREATE --------------------------------------------------------------->
@login_required
@permission_required('sicoapp.add_fueltap', raise_exception=True)
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
@permission_required('sicoapp.change_fueltap', raise_exception=True)
def fueltap_update_view(request, id):
    fueltap = get_object_or_404(FuelTap, pk=id)

    if request.method == 'POST':
        form = FuelTapForm(request.POST, instance=fueltap)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Actualización exitosa!')
            return redirect('sicomec:fueltap_list')
    else:
        form = FuelTapForm(instance=fueltap)

    return render(request, 'fueltaps/fueltap_update.html', {'form': form, })

# LIST ------------------------------------------------------------------->
@login_required
@permission_required('sicoapp.view_fueltap', raise_exception=True)
def fueltap_list_view(request):
    results = FuelTap.objects.all()

    return render(request, 'fueltaps/fueltap_list.html', {'fueltaps': results, })

# DELETE ------------------------------------------------------------------>
@login_required
@permission_required('sicoapp.delete_fueltap', raise_exception=True)
def fueltap_delete_view(request, id):
    fueltap = get_object_or_404(FuelTap, pk=id)

    if BuyOrder.objects.filter(fueltap=fueltap.pk).exists():
        messages.warning(request, 'Proveedor tiene orden de compra asociada')
    
    else:
        fueltap.delete()
        messages.success(request, '¡Registro eliminado!')

    return redirect('sicomec:fueltap_list')  



# ************************************ BUY ORDER VIEWS ************************************

# CREATE --------------------------------------------------------------->
@login_required
@permission_required('sicoapp.add_buyorder', raise_exception=True)
def buy_order_create_view(request):
    if request.method == 'POST':
        form = BuyOrderForm(request.POST)
        if form.is_valid():

            stock_value = form.cleaned_data['stock']
            buy_order_instance = form.save(commit=False)
            buy_order_instance.residue = stock_value
            buy_order_instance.user = request.user

            try:
                buy_order_instance.save()
                messages.success(request, '¡Registro exitoso!')
                return redirect('sicomec:buy_order_list')  
            except IntegrityError:
                messages.warning(request, 'Orden de compra ya existe')
                return redirect('sicomec:buy_order_create')
    else:
        form = BuyOrderForm()
    
    return render(request, 'buy_orders/buy_order_create.html', {'form': form})

# UPDATE ----------------------------------------------------------------->
@login_required
@permission_required('sicoapp.change_buyorder', raise_exception=True)
def buy_order_update_view(request, id):
    buy_order = get_object_or_404(BuyOrder, pk=id)

    if request.method == 'POST':
        form = BuyOrderForm(request.POST, instance=buy_order)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Actualización exitosa!')
            return redirect('sicomec:buy_order_list')
    else:
        formatted_date = buy_order.date.strftime('%Y-%m-%d')
        form = BuyOrderForm(instance=buy_order, initial={'date': formatted_date})

    return render(request, 'buy_orders/buy_order_update.html', {'form': form, })

# LIST ------------------------------------------------------------------->
@login_required
@permission_required('sicoapp.view_buyorder', raise_exception=True)
def buy_order_list_view(request):
    results = BuyOrder.objects.all()

    return render(request, 'buy_orders/buy_order_list.html', {'buy_orders': results, })

# DELETE ------------------------------------------------------------------>
@login_required
@permission_required('sicoapp.delete_buyorder', raise_exception=True)
def buy_order_delete_view(request, id):
    buy_order = get_object_or_404(BuyOrder, pk=id)

    if FuelOrder.objects.filter(order=buy_order.pk).exists():
        messages.warning(request, 'Orden de compra tiene pedido de combustible asociada')
    
    else:
        buy_order.delete()
        messages.success(request, '¡Registro eliminado!')

    return redirect('sicomec:buy_order_list')  



# ************************************ FUEL ORDER VIEWS ************************************

# CREATE --------------------------------------------------------------->
@login_required
@permission_required('sicoapp.add_fuelorder', raise_exception=True)
def fuel_order_create_view(request):
    if request.method == 'POST':
        form = FuelOrderForm(request.POST)
        if form.is_valid():
            fuel_order = form.save(commit=False)
            form.instance.user = request.user

            try:
                buy_order = BuyOrder.objects.get(id=fuel_order.order.id)
            except BuyOrder.DoesNotExist:
                messages.error(request, 'Orden de compra no encontrada')
                return redirect('sicomec:fuel_order_list')

            if fuel_order.fuel_loan and fuel_order.fuel_return:
                messages.warning(request, 'No puedes marcar ambos, lluqsin y kutimun')
                return redirect('sicomec:fuel_order_list')

            total_loan = FuelOrder.objects.filter(order=buy_order, fuel_loan=True).aggregate(Sum('quantity'))['quantity__sum'] or 0
            total_return = FuelOrder.objects.filter(order=buy_order, fuel_return=True).aggregate(Sum('quantity'))['quantity__sum'] or 0

            if fuel_order.fuel_return:
                if fuel_order.quantity + total_return > total_loan:
                    messages.warning(request, f'Kutimun ({fuel_order.quantity}) excede a Lluqsin ({total_loan})')
                    return redirect('sicomec:fuel_order_list')
                new_residue = buy_order.residue + fuel_order.quantity
            else:  
                new_residue = buy_order.residue - fuel_order.quantity

            if new_residue < 0:
                messages.warning(request, '¡Saldo insuficiente!')
                return redirect('sicomec:fuel_order_list')

            buy_order.residue = new_residue
            buy_order.save()
            fuel_order.residue = new_residue
            fuel_order.save()

            messages.success(request, '¡Registro exitoso!')
            return redirect(f"{request.path}?success=true&fuel_order_id={fuel_order.id}")

    else:
        form = FuelOrderForm()

    return render(request, 'fuel_orders/fuel_order_create.html', {'form': form})

# UPDATE ----------------------------------------------------------------->
# @login_required
# def fuel_order_update_view(request, id):
#     fuel_order = get_object_or_404(FuelOrder, pk=id)
#     query = request.GET.get('q', '')

#     if request.method == 'POST':
#         form = FuelOrderForm(request.POST, instance=fuel_order)
#         if form.is_valid():
#             form.save()
#             messages.success(request, '¡Actualización exitosa!')
#             return redirect(f"{reverse('sicomec:fuel_order_list')}?q={query}")
#     else:
#         formatted_date = fuel_order.date.strftime('%Y-%m-%d')
#         form = FuelOrderForm(instance=fuel_order, initial={'date': formatted_date})

#     return render(request, 'fuel_orders/fuel_order_update.html', {'form': form, 'query': query,})

# LIST ------------------------------------------------------------------->
@login_required
@permission_required('sicoapp.view_fuelorder', raise_exception=True)
def fuel_order_list_view(request):
    results = FuelOrder.objects.all()

    for result in results:
        result.show_buttons = not (result.canceled or result.fuel_loan or result.fuel_return)

    return render(request, 'fuel_orders/fuel_order_list.html', {'fuel_orders': results, })

# GENEREATE PDF ------------------------------------------------------------------>
@login_required
def generate_fuel_order_pdf(request, id):
    fuel_order = get_object_or_404(FuelOrder, pk=id)

    base_url = 'file:///C:/sicomec/'
    current_date = timezone.localtime(timezone.now(), timezone=pytz.timezone('America/Lima'))
    date_print = format_datetime(current_date, format="d'/'MM'/'yyyy HH:mm", locale='es')

    data = {
        'date': date_print,
        'base_url':base_url,
        'fuel_order': fuel_order,
        'current_date': current_date,
    }

    html_string = render_to_string('fuel_orders/fuel_order_template_pdf.html', data)

    filename = current_date.strftime('%d-%m-%Y %H.%M') + "_pedido de combustible.pdf"
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response

# DELETE ------------------------------------------------------------------>
@login_required
@permission_required('sicoapp.delete_fuelorder', raise_exception=True)
def fuel_order_delete_view(request, id):

    fuel_order = get_object_or_404(FuelOrder, pk=id)

    if not fuel_order.canceled:
            buy_order = BuyOrder.objects.get(id=fuel_order.order.id)
            
            buy_order.residue += fuel_order.quantity
            buy_order.save()
            
            fuel_order.canceled = True
            fuel_order.save()

            messages.success(request, '¡Registro Anulado!')
            return redirect('sicomec:fuel_order_list')  

# CONTROL CARD ------------------------------------------------------------------>
@login_required
def control_card_view(request):
    return render(request, 'fuel_orders/fuel_order_control_card.html')

# CONTROL CARD PDF ------------------------------------------------------------------>
@login_required
def generate_control_card_pdf(request, order_id):
    orders = FuelOrder.objects.filter(order=order_id)
    buy_order = get_object_or_404(BuyOrder, id=order_id)

    base_url = request.build_absolute_uri('/')
    img_drta = base_url + static('/images/drta.png')
    img_sicomec = base_url + static('/images/logo_sicomec_lg.png')

    current_date = timezone.localtime(timezone.now(), timezone=pytz.timezone('America/Lima'))
    date_print = format_datetime(current_date, format="d'/'MM'/'yyyy HH:mm", locale='es')

    data = {
        'date': date_print,
        'orders': orders,
        'buy_order': buy_order,
        'current_date': current_date,
        'stock': buy_order.stock,
        'residue': buy_order.residue,
        'img_drta': img_drta,
        'img_sicomec': img_sicomec,
    }

    html_string = render_to_string('fuel_orders/fuel_order_control_card_template_pdf.html', data)

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=Orde de compra_{buy_order.order}'
    return response



# ************************************ BALLOT VIEWS ************************************

# CREATE --------------------------------------------------------------->
@login_required
@permission_required('sicoapp.add_ballot', raise_exception=True)
def ballot_create_view(request):
    if request.method == 'POST':
        form = BallotForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            ballot = form.save() 
            messages.success(request, '¡Registro exitoso!')
            return redirect(f"{request.path}?success=true&ballot_id={ballot.id}")
    else:
        form = BallotForm()

    return render(request, 'ballots/ballot_create.html', {'form': form})

# UPDATE ----------------------------------------------------------------->
@login_required
@permission_required('sicoapp.change_ballot', raise_exception=True)
def ballot_update_view(request, id):
    ballot = get_object_or_404(Ballot, pk=id)

    if request.method == 'POST':
        form = BallotForm(request.POST, instance=ballot)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Actualización exitosa!')
            return redirect('sicomec:ballot_list_scheduled')
        else:
            print(form.errors) 
    else:
        form = BallotForm(instance=ballot, initial={
                            'exit_date': ballot.exit_date.strftime('%Y-%m-%d'),
                            })

    return render(request, 'ballots/ballot_update.html', {'form': form, })

# LIST SCHEDULED------------------------------------------------------------------->
@login_required
@permission_required('sicoapp.view_ballot', raise_exception=True)
def ballot_list_scheduled_view(request):
    
    results = Ballot.objects.filter(
        return_date__isnull=True,
        return_time__isnull=True
    )

    return render(request, 'ballots/ballot_list_scheduled.html', {'ballots': results, })

# LIST COMPLETE------------------------------------------------------------------->
@login_required
@permission_required('sicoapp.view_ballot', raise_exception=True)
def ballot_list_complete_view(request):
    results = Ballot.objects.filter(
        return_date__isnull=False,
        return_time__isnull=False,
    )

    return render(request, 'ballots/ballot_list_complete.html', { 'ballots': results, })

# MARK RETURN------------------------------------------------------------------->
@login_required
@permission_required('sicoapp.change_ballot', raise_exception=True)
def ballot_mark_return_view(request):
    query = request.GET.get('q', '').strip()
    search_performed = False
    results = []
    message = ""
    ballot_count = 0

    if query:
        search_performed = True
        results = Ballot.objects.filter(
            (Q(code__iexact=query) | Q(plate__plate__iexact=query)) &
            Q(return_date__isnull=True) &
            Q(return_time__isnull=True)
        )
        
        if results.exists():
            ballot_count = results.count()
        else:
            message = "No se encontraron resultados"

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
@permission_required('sicoapp.change_ballot', raise_exception=True)
def update_return_datetime(request, id):
    ballot = get_object_or_404(Ballot, pk=id)

    lima_tz = pytz.timezone('America/Lima')
    current_time = timezone.now().astimezone(lima_tz)

    exit_datetime = timezone.make_aware(
        datetime.combine(ballot.exit_date, ballot.exit_time), 
        lima_tz
    )

    if current_time < exit_datetime:
        messages.warning(request, 'No se puede retornar antes de la salida')
        return redirect('sicomec:ballot_mark_return')

    else:
        ballot.return_date = current_time.date()
        ballot.return_time = current_time.time()
        ballot.save()
        messages.success(request, '¡Retorno marcado!')

    return redirect('sicomec:ballot_list_complete')

# GENEREATE PDF ------------------------------------------------------------------>
@login_required
def generate_ballot_pdf(request, id):
    ballot = get_object_or_404(Ballot, pk=id)
    vehicle = get_object_or_404(Vehicle, plate=ballot.plate)
    typeVehicle = vehicle.type.name


    base_url = 'file:///C:/sicomec/'
    current_date = timezone.localtime(timezone.now(), timezone=pytz.timezone('America/Lima'))
    date_print = format_datetime(current_date, format="d'/'MM'/'yyyy HH:mm", locale='es')

    data = {
        'date': date_print,
        'base_url':base_url,
        'ballot': ballot,
        'current_date': current_date,
        'typeVehicle': typeVehicle,
    }

    html_string = render_to_string('ballots/ballot_template_pdf.html', data)

    filename = current_date.strftime('%d-%m-%Y %H.%M') + "_papeleta de salida.pdf"
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response

# DELETE ------------------------------------------------------------------>
@login_required
@permission_required('sicoapp.delete_ballot', raise_exception=True)
def ballot_delete_view(request, id):
    ballot = get_object_or_404(Ballot, pk=id)

    ballot.delete()
    messages.success(request, '¡Registro eliminado!')

    redirect_to = request.GET.get('redirect_to', 'scheduled')
    if redirect_to == 'completed':
        return redirect('sicomec:ballot_list_complete')
    else:
        return redirect('sicomec:ballot_list_scheduled')

# REPORT ------------------------------------------------------------------>
@login_required
def ballot_report_view(request):
    ballots = Ballot.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        filtered_ballots = ballots.filter(
            exit_date__range=[start_date, end_date]
        )
    elif start_date:
        filtered_ballots = ballots.filter(exit_date__gte=start_date)
    elif end_date:
        filtered_ballots = ballots.filter(exit_date__lte=end_date)
    else:
        filtered_ballots = ballots.none()
    
    filtered_ballots = filtered_ballots.order_by('exit_date')

    # Si se solicita la generación de PDF
    if 'generate_pdf' in request.GET:
        base_url = 'file:///C:/sicomec/'
        current_date = timezone.localtime(timezone.now(), timezone=pytz.timezone('America/Lima'))
        date_print = format_datetime(current_date, format="d'/'MM'/'yyyy HH:mm", locale='es')

        data = {
            'date': date_print,
            'base_url': base_url,
            'ballots': filtered_ballots,
        }

        html_string = render_to_string('ballots/ballot_report_template_pdf.html', data)
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="reporte_papeletas.pdf"'
        return response

    return render(request, 'ballots/ballot_report.html')
    


# NOTIFICATION ------------------------------------------------------------------->

# LIST ------------------------------------------------------------------>
@login_required
@permission_required('sicoapp.view_notification', raise_exception=True)
def notification_list_view(request):
    current_date = timezone.localtime(timezone.now(), timezone=pytz.timezone('America/Lima'))
    date_print = format_datetime(current_date, format="d'-'MM'-'yyyy HH:mm", locale='es')

    drivers = Notification.objects.filter(
        ~Q(license__isnull=True), 
        ~Q(license='')           
        )
    vehicle_soats = Notification.objects.filter(
        ~Q(soat__isnull=True), 
        ~Q(soat='')           
        )
    vehicle_citvs = Notification.objects.filter(
        ~Q(citv__isnull=True), 
        ~Q(citv='')           
        )
    
    count_drivers = drivers.count()
    count_vehicle_soats = vehicle_soats.count()
    count_vehicle_citvs = vehicle_citvs.count()

    data = {
        'drivers': drivers,
        'vehicle_soats': vehicle_soats,
        'vehicle_citvs': vehicle_citvs,
        'count_drivers': count_drivers,
        'count_vehicle_soats': count_vehicle_soats,
        'count_vehicle_citvs': count_vehicle_citvs,
        'date_print': date_print,
    }

    return render(request, 'notifications/notification_list.html', data)

# COUNT ------------------------------------------------------------------>
@login_required
def notification_count_view(request):
    drivers = Notification.objects.filter(
        ~Q(license__isnull=True), 
        ~Q(license='')           
        ).count()
    vehicle_soats = Notification.objects.filter(
        ~Q(soat__isnull=True), 
        ~Q(soat='')           
        ).count()
    vehicle_citvs = Notification.objects.filter(
        ~Q(citv__isnull=True), 
        ~Q(citv='')           
        ).count()
    
    total_count = drivers + vehicle_soats + vehicle_citvs

    return JsonResponse({'count': total_count})



# ************************************ GETTERS VIEWS ************************************

# GET DRIVER DETAILS ------------------------------------------------------------------>
@login_required
def get_driver_details_view(request, id):
    try:
        driver = get_object_or_404(Driver.objects.select_related('category'), pk=id)

        data = {
            'license': driver.license,
            'category': driver.category.name,
        }
        return JsonResponse(data)
    except Driver.DoesNotExist:
        return JsonResponse({'error': 'Conductor no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# GET VEHICLE DETAILS ------------------------------------------------------------------>
@login_required
def get_vehicle_details_view(request, id):
    try:
        vehicle = get_object_or_404(Vehicle.objects.only('brand', 'name', 'type'), pk=id) 
        data = {
            'brand': vehicle.brand,
            'vehicle': vehicle.name,
            'type':vehicle.type.name,
        }

        return JsonResponse(data)
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehículo no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# GET BUY ORDER DETAILS ------------------------------------------------------------------>
@login_required
def get_buy_order_details_view(request, id_buy_order):
    try:
        buy_order = get_object_or_404(BuyOrder.objects.select_related('fueltap', 'fuel'), pk=id_buy_order)
        formatted_stock = "{:,}".format(buy_order.stock)
        formatted_residue = "{:,}".format(buy_order.residue)

        data = {
            'user_area': buy_order.user_area,
            'fueltap': buy_order.fueltap.business_name,
            'fuel': buy_order.fuel.name,
            'stock': formatted_stock,
            'residue': formatted_residue,
        }
        return JsonResponse(data)
    except BuyOrder.DoesNotExist:
        return JsonResponse({'error': 'Orden de compra no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
# GET UUID BUY ORDER ------------------------------------------------------------------>
@login_required
def get_buy_order_uuid_view(request, order_identifier):
    if not re.match(r'^\d{1,7}(GR|GP|DS)$', order_identifier):
        return JsonResponse({'error': 'Número de orden inválido'}, status=400)
    
    try:
        buy_order = get_object_or_404(BuyOrder, order=order_identifier)
        data = {'uuid': str(buy_order.id)}
        return JsonResponse(data)

    except Http404:
        return JsonResponse({'error': 'Orden de compra no encontrada'}, status=404)

    except ValueError as e:
        return JsonResponse({'error': 'Identificador de orden inválido'}, status=400)

    except Exception as e:
        return JsonResponse({'error': f'Se produjo un error inesperado: {str(e)}'}, status=500)



# GET FUEL ORDERS ------------------------------------------------------------------>
@login_required
def get_fuel_orders_view(request, id_buy_order):
    try:
        fuel_orders = FuelOrder.objects.filter(order=id_buy_order).select_related('vehicle', 'driver')
        
        data = list(fuel_orders.values(
            'date',
            'quantity',
            'residue',
            'plate__plate',
            'vehicle',
            'brand',
            'driver__name',
            'driver__last_name',
            'voucher',
            'code',
            'canceled',
            'fuel_loan',
            'fuel_return',
        ))

        for item in data:
            if item['date']:
                item['date'] = item['date'].strftime('%d-%m-%Y')
            
            if item['residue']:
                item['residue'] = "{:,}".format(item['residue'])

        return JsonResponse({'fuel_orders': data}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



# ************************************ ERROR VIEWS ************************************
@login_required
def error_404(request, exception):
    return render(request, '404.html', {})

@login_required
def error_403(request, exception):
    return render(request, '403.html', status=403)
