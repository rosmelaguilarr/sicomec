from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from .models import Driver, Vehicle, FuelTap, Ballot, Notification, BuyOrder, FuelOrder
from .forms import DriverForm, VehicleForm, FuelTapForm, BallotForm, BuyOrderForm, FuelOrderForm
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
import pytz
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from babel.dates import format_datetime
from django.http import JsonResponse
from django.utils.dateformat import format



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
                request.session['alertShow'] = True  # Set alertShow to True
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
    request.session['alertShow'] = False  # Set alertShow to False
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

# DELETE ------------------------------------------------------------------>
@login_required
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
                            # 'production': vehicle.production.strftime('%Y-%m-%d'),
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

# DELETE ------------------------------------------------------------------>
@login_required
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

    if BuyOrder.objects.filter(fueltap=fueltap.pk).exists():
        messages.warning(request, 'Proveedor tiene orden de compra asociada')
    
    else:
        fueltap.delete()
        messages.success(request, '¡Registro eliminado!')

    return redirect('sicomec:fueltap_list')  



# ************************************ BUY ORDER VIEWS ************************************

# CREATE --------------------------------------------------------------->
@login_required
def buy_order_create_view(request):
    if request.method == 'POST':
        form = BuyOrderForm(request.POST)
        if form.is_valid():

            stock_value = form.cleaned_data['stock']
            buy_order_instance = form.save(commit=False)
            buy_order_instance.residue = stock_value
            buy_order_instance.user = request.user
            buy_order_instance.save()

            messages.success(request, '¡Registro exitoso!')
            return redirect('sicomec:buy_order_list')  
    else:
        form = BuyOrderForm()
    
    return render(request, 'buy_orders/buy_order_create.html', {'form': form})

# UPDATE ----------------------------------------------------------------->
@login_required
def buy_order_update_view(request, id):
    buy_order = get_object_or_404(BuyOrder, pk=id)
    query = request.GET.get('q', '')

    if request.method == 'POST':
        form = BuyOrderForm(request.POST, instance=buy_order)
        if form.is_valid():
            form.save()
            # stock_value = form.cleaned_data['stock']
            # buy_order_instance = form.save(commit=False)
            # buy_order_instance.residue = stock_value
            # buy_order_instance.user = request.user
            # buy_order_instance.save()

            messages.success(request, '¡Actualización exitosa!')
            return redirect(f"{reverse('sicomec:buy_order_list')}?q={query}")
    else:
        formatted_date = buy_order.date.strftime('%Y-%m-%d')
        form = BuyOrderForm(instance=buy_order, initial={'date': formatted_date})

    return render(request, 'buy_orders/buy_order_update.html', {'form': form, 'query': query,})

# LIST ------------------------------------------------------------------->
@login_required
def buy_order_list_view(request):
    query = request.GET.get('q', '').strip()
    search_performed = False
    results = []
    message = ""
    buy_order_count = 0

    if query:
        search_performed = True
        results = BuyOrder.objects.filter(
            Q(order__icontains=query) |
            Q(user_area__icontains=query)
        )
        if results.exists():
            buy_order_count = results.count()
        else:
            message = "No se encontraron órdenes de servicio con esos criterios"
    else:
        results = BuyOrder.objects.all()
        buy_order_count = results.count()

    return render(request, 'buy_orders/buy_order_list.html', 
                {
                    'buy_orders': results,
                    'query': query,
                    'search_performed':search_performed,
                    'buy_order_count': buy_order_count,
                    'message': message,
                })

# DELETE ------------------------------------------------------------------>
@login_required
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
def fuel_order_create_view(request):

    if request.method == 'POST':
        form = FuelOrderForm(request.POST)
        if form.is_valid():
            fuel_order = form.save(commit=False)
            form.instance.user = request.user

            buy_order = BuyOrder.objects.get(id=fuel_order.order.id)

            if fuel_order.fuel_return:
                new_residue = buy_order.residue + fuel_order.quantity
                buy_order.residue = new_residue
                fuel_order.residue = new_residue

            else:
                new_residue = buy_order.residue - fuel_order.quantity
                buy_order.residue = new_residue
                fuel_order.residue = new_residue

            buy_order.save()
            fuel_order.save()

            messages.success(request, '¡Registro exitoso!')
            return redirect('sicomec:fuel_order_list')
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
def fuel_order_list_view(request):
    query = request.GET.get('q', '').strip()
    search_performed = False
    results = []
    message = ""
    fuel_order_count = 0

    if query:
        search_performed = True
        results = FuelOrder.objects.filter(
            Q(fueltap__business_name__icontains=query) |
            Q(driver__name__icontains=query)|
            Q(driver__last_name__icontains=query)
        )
        if results.exists():
            fuel_order_count = results.count()
        else:
            message = "No se encontraron órdenes de compra con esos criterios"
    else:
        results = FuelOrder.objects.all()
        fuel_order_count = results.count()

    for result in results:
        result.show_buttons = not (result.canceled or result.fuel_loan or result.fuel_return)

    return render(request, 'fuel_orders/fuel_order_list.html', 
                {
                    'fuel_orders': results,
                    'query': query,
                    'search_performed':search_performed,
                    'fuel_order_count': fuel_order_count,
                    'message': message,
                })

# GENEREATE PDF ------------------------------------------------------------------>
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
    buy_orders = BuyOrder.objects.all()

    return render(request, 'fuel_orders/fuel_order_control_card.html', 
                {
                    'buy_orders': buy_orders,
                })



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
            print(form.errors) 
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
            (Q(code__icontains=query) | Q(plate__plate__icontains=query)) &
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
            (Q(code__icontains=query) | Q(plate__plate__icontains=query)) &
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
            return_time__isnull=False,
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
            (Q(code__iexact=query) | Q(plate__plate__iexact=query)) &
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
    ballot = get_object_or_404(Ballot, pk=id)

    lima_tz = pytz.timezone('America/Lima')
    current_time = timezone.now().astimezone(lima_tz)
    ballot.return_date = current_time.date()
    ballot.return_time = current_time.time()

    ballot.save()
    messages.success(request, '¡Retorno marcado!')
    return redirect(f"{reverse('sicomec:ballot_mark_return')}")

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

    html_string = render_to_string('ballots/ballot_template_pdf.html', data)

    filename = current_date.strftime('%d-%m-%Y %H.%M') + "_papeleta de salida.pdf"
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response

# DELETE ------------------------------------------------------------------>
@login_required
def ballot_delete_view(request, id):
    ballot = get_object_or_404(Ballot, pk=id)

    ballot.delete()
    messages.success(request, '¡Registro eliminado!')

    redirect_to = request.GET.get('redirect_to', 'scheduled')
    if redirect_to == 'completed':
        return redirect('sicomec:ballot_list_complete')
    else:
        return redirect('sicomec:ballot_list_scheduled')



# NOTIFICATION------------------------------------------------------------------->

# LIST ------------------------------------------------------------------>
@login_required
def notification_list_view(request):
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
    }

    return render(request, 'notifications/notification_list.html', data)

# COUNT ------------------------------------------------------------------>
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

# DELETE ------------------------------------------------------------------>
def notification_delete_view(request, id):
    notification = get_object_or_404(Notification, pk=id)

    notification.delete()
    messages.success(request, '¡Registro eliminado!')

    return redirect('sicomec:notification_list')  

# ************************************ GETTERS VIEWS ************************************

# GET DRIVER DETAILS ------------------------------------------------------------------>
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
def get_vehicle_details_view(request, id):
    try:
        vehicle = get_object_or_404(Vehicle.objects.only('brand', 'name'), pk=id) 
        data = {
            'brand': vehicle.brand,
            'vehicle': vehicle.name
        }

        return JsonResponse(data)
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehículo no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# GET BUY ORDER DETAILS ------------------------------------------------------------------>
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

# GET FUEL ORDERS ------------------------------------------------------------------>
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

def error_404(request, exception):
    return render(request, '404.html', {})

def error_403(request, exception):
    return render(request, '403.html', status=403)
