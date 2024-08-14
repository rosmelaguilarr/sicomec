from django.db import models
from django.contrib.auth.models import User
import os
from django.core.validators import MinValueValidator
import uuid
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import datetime


# STATIC MODELS --------------------------------------------------------------------

class LicenseCategory(models.Model):
    name = models.CharField(max_length=6, null=False, blank=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "LicenseCategory"
        verbose_name = "Categoría de Licencia"
        verbose_name_plural = "Categoría de Licencias"
    
class Fuel(models.Model):
    name = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "Fuel"
        verbose_name = "Tipo de Combustible"
        verbose_name_plural = "Tipo de Combustibles"

class TypeVehicle(models.Model):
    name = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "TypeVehicle"
        verbose_name = "Tipo de Vehículo"
        verbose_name_plural = "Tipo de Vehículos"


# DRIVER MODEL --------------------------------------------------------------------

dni_validator = RegexValidator(
    regex=r'^[0-9]{8}$', 
    message="El DNI debe ser numérico de 8 dígitos"
)

license_validator = RegexValidator(
    regex=r'^[A-Z][0-9]{8}$',
    message="La licencia debe comenzar con una letra (A-Z) seguido del DNI"
)

class Driver(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dni = models.CharField(max_length=8, verbose_name='DNI', unique=True, validators=[dni_validator])
    name = models.CharField(max_length=20, verbose_name='Nombres', null=False, blank=False)
    last_name = models.CharField(max_length=30, verbose_name='Apellidos', null=False, blank=False)
    license = models.CharField(max_length=9, verbose_name='N° Licencia', unique=True, validators=[license_validator])
    category = models.ForeignKey(LicenseCategory, on_delete=models.PROTECT, verbose_name='Categoría')
    expiration = models.DateField(verbose_name='Venc. Licencia', auto_now=False)
    validity = models.BooleanField(default=True)
    available = models.BooleanField(default=True, verbose_name='Disponible')
    justify = models.TextField(verbose_name='Justificación',null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} {self.last_name}'

    class Meta:
        db_table = "Driver"
        verbose_name = "Conductor"
        verbose_name_plural = "Conductores"

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.upper()
        if self.last_name:
            self.last_name = self.last_name.upper()
        if self.license:
            self.license = self.license.upper()
        if self.justify:
            self.justify = self.justify.upper()
        super(Driver, self).save(*args, **kwargs)



# VEHICLE MODEL --------------------------------------------------------------------

class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plate = models.CharField(max_length=6, verbose_name='Placa', null=False, blank=False)
    type = models.ForeignKey(TypeVehicle, on_delete=models.PROTECT, verbose_name='Tipo')
    name = models.CharField(max_length=30, verbose_name='Vehículo', null=False, blank=False)
    brand = models.CharField(max_length=20, verbose_name='Marca', null=False, blank=False)
    chassis = models.CharField(max_length=17, verbose_name='Chasis', null=False, blank=False)
    model = models.CharField(max_length=20, verbose_name='Modelo', null=False, blank=False)
    production = models.IntegerField(verbose_name='Fabricación',  null=False, blank=False)
    fuel = models.ForeignKey(Fuel, on_delete=models.PROTECT, verbose_name='Combustible')
    mileage = models.PositiveIntegerField(verbose_name='Kilometraje',default=0, null=True, blank=True)
    hourometer = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Horómetro', default=0, null=True, blank=True)
    soat = models.DateField(verbose_name='Emisión SOAT', auto_now=False)
    citv = models.DateField(verbose_name='Emisión CITV', auto_now=False)
    available = models.BooleanField(default=True, verbose_name='Disponible')
    justify = models.TextField(verbose_name='Justificación',null=True, blank=True)
    maintenance = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.plate
    
    class Meta:
        db_table = "Vehicle"
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
    
    def save(self, *args, **kwargs):
        if self.plate:
            self.plate = self.plate.upper()
        if self.name:
            self.name = self.name.upper()
        if self.brand:
            self.brand = self.brand.upper()
        if self.chassis:
            self.chassis = self.chassis.upper()
        if self.model:
            self.model = self.model.upper()
        if self.justify:
            self.justify = self.justify.upper()
        super(Vehicle, self).save(*args, **kwargs)



# FUELTAP MODEL --------------------------------------------------------------------

ruc_validator = RegexValidator(
    regex=r'^[0-9]{11}$', 
    message="El RUC debe ser numérico de 11 dígitos"
)

email_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    message="Correo electrónico incorrecto"
)

class FuelTap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ruc = models.CharField(max_length=11, verbose_name='RUC', unique=True,  null=False, blank=False, validators=[ruc_validator])
    business_name = models.CharField(max_length=70, verbose_name='Razón Social', null=False, blank=False)
    address = models.CharField(max_length=50, verbose_name='Dirección', null=False, blank=False)
    email =  models.CharField(max_length=50, verbose_name='Email',  null=True, blank=True, validators=[email_validator])
    phone = models.CharField(max_length=30, verbose_name='Celular',  null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.business_name
    
    class Meta:
        db_table = "FuelTap"
        verbose_name = "Grifo"
        verbose_name_plural = "Grifos"
    
    def save(self, *args, **kwargs):
        if self.business_name:
            self.business_name = self.business_name.upper()
        if self.address:
            self.address = self.address.upper()
        if self.email:
            self.email = self.email.upper()
        super(FuelTap, self).save(*args, **kwargs)



# BUY ORDER MODEL --------------------------------------------------------------------

seven_digit_with_optional_suffix_regex = r'^\d{7}(?:GR|GP|DS)?$'

order_validator = RegexValidator(
    regex=seven_digit_with_optional_suffix_regex, 
    message="Orden de compra debe ser numérico de 7 dígitos, seguido opcionalmente por GR|GP|DS"
)

class BuyOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order =  models.CharField(max_length=9, verbose_name='N° Orden', unique=True,  null=False, blank=False, validators=[order_validator])
    user_area = models.TextField(verbose_name='Área Usuaria',null=False, blank=False)
    fueltap = models.ForeignKey(FuelTap, on_delete=models.PROTECT, verbose_name='Proveedor')
    fuel = models.ForeignKey(Fuel, on_delete=models.PROTECT, verbose_name='Combustible')
    stock = models.PositiveIntegerField(verbose_name='Cantidad',default=0, null=False, blank=False)
    residue = models.PositiveIntegerField(default=0)
    date = models.DateField(verbose_name='Fecha', auto_now=False)
    detail = models.TextField(verbose_name='Detalle',null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.order
    
    class Meta:
        db_table = "BuyOrder"
        verbose_name = "Número de Orden"
        verbose_name_plural = "Números de Órdenes"
    
    def save(self, *args, **kwargs):
        if self.user_area:
            self.user_area = self.user_area.upper()
        if self.detail:
            self.detail = self.detail.upper()
        super(BuyOrder, self).save(*args, **kwargs)



# FUEL ORDER MODEL --------------------------------------------------------------------

voucher_validator = RegexValidator(
    regex=r'^[0-9]{7}$', 
    message="El vale debe ser numérico de 7 dígitos"
)

class FuelOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True, editable=False) 
    fueltap = models.CharField(max_length=70, verbose_name='Proveedor', null=False, blank=False)
    order = models.ForeignKey(BuyOrder, on_delete=models.PROTECT, verbose_name='N° Orden')
    user_area = models.TextField(verbose_name='Área Usuaria', blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, verbose_name='Conductor')
    plate = models.ForeignKey(Vehicle, on_delete=models.PROTECT, verbose_name='Placa')
    brand = models.CharField(max_length=50, null=False, blank=False, verbose_name='Marca')
    vehicle = models.CharField(max_length=50, null=False, blank=False, verbose_name='Vehículo')
    place = models.CharField(max_length=70, verbose_name='Destino', null=False, blank=False)
    reason = models.TextField(verbose_name='Motivo', null=False, blank=False)
    quantity = models.PositiveIntegerField(verbose_name='Cantidad',default=0, null=False, blank=False)
    residue = models.PositiveIntegerField(default=0)
    fuel = models.CharField(max_length=10, verbose_name='Combustible', null=False, blank=False)
    voucher = models.CharField(max_length=7, verbose_name='N° Vale', null=False, blank=False, validators=[voucher_validator])
    date = models.DateField(verbose_name='Fecha', auto_now=False)
    canceled = models.BooleanField(default=False)
    fuel_loan = models.BooleanField(default=False, verbose_name='Préstamo')
    fuel_return = models.BooleanField(default=False, verbose_name='Devolución')
    detail = models.TextField(verbose_name='Detalle', null=True, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.code
    
    class Meta:
        db_table = "FuelOrder"
        verbose_name = "Pedido Combustible"
        verbose_name_plural = "Pedidos Combustible"
    
    def save(self, *args, **kwargs):
        if self.place:
            self.place = self.place.upper()
        if self.reason:
            self.reason = self.reason.upper()
        if not self.code:
            if not self.code:
                current_year = str(timezone.now().year)[-2:] 
                last_fuel_order = FuelOrder.objects.filter(code__startswith=f"{current_year}C").order_by('-code').first()

                if last_fuel_order:
                    last_number = int(last_fuel_order.code[3:9])
                    new_number = last_number + 1
                else:
                    new_number = 1

                self.code = f"{current_year}C{new_number:06d}"
        super(FuelOrder, self).save(*args, **kwargs)



# BALLOT MODEL --------------------------------------------------------------------

class Ballot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True, editable=False)
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT, verbose_name='Conductor')
    driver_license = models.CharField(max_length=9, verbose_name='N° Licencia')
    driver_category = models.CharField(max_length=6, verbose_name='Categoría')
    drive_to = models.CharField(max_length=70, verbose_name='Sírvase conducir', null=False, blank=False)
    plate = models.ForeignKey(Vehicle, on_delete=models.PROTECT, verbose_name='Placa')
    vehicle_name = models.CharField(max_length=30, verbose_name='Vehículo')
    vehicle_brand = models.CharField(max_length=20, verbose_name='Marca')
    place = models.CharField(max_length=70, verbose_name='Destino', null=False, blank=False)
    reason = models.TextField(verbose_name='Motivo', null=False, blank=False)
    exit_date = models.DateField(verbose_name='Fecha Salida', auto_now=False)
    exit_time = models.TimeField(verbose_name='Hora Salida')
    return_date = models.DateField(verbose_name='Fecha Retorno', default=None, auto_now=False, null=True, blank=True)
    return_time = models.TimeField(verbose_name='Hora Retorno', default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.code

    class Meta:
        db_table = "Ballot"
        verbose_name = "Papeleta"
        verbose_name_plural = "Papeletas"

    def save(self, *args, **kwargs):
        if self.drive_to:
            self.drive_to = self.drive_to.upper()
        if self.place:
            self.place = self.place.upper()
        if self.reason:
            self.reason = self.reason.upper()

        if not self.code:
            if not self.code:
                doc_year = str(timezone.now().year)[-2:] 
                last_ballot = Ballot.objects.filter(code__startswith=f"{doc_year}P").order_by('-code').first()

                if last_ballot:
                    last_number = int(last_ballot.code[3:9])
                    new_number = last_number + 1
                else:
                    new_number = 1

                self.code = f"{doc_year}P{new_number:06d}"
        super(Ballot, self).save(*args, **kwargs)



# NOTIFICATION MODEL --------------------------------------------------------------------

class Notification(models.Model):
    license = models.CharField(max_length=30, null=True, blank=True)
    driver = models.CharField(max_length=30, null=True, blank=True)
    expiration = models.CharField(max_length=10, null=True, blank=True)
    plate = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    brand = models.CharField(max_length=30, null=True, blank=True)
    soat = models.CharField(max_length=10, null=True, blank=True)
    citv = models.CharField(max_length=10, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created
    
    def get_formatted_expiration(self):
        return self.format_date(self.expiration)
        
    def get_formatted_soat(self):
        return self.format_date(self.soat)

    def get_formatted_citv(self):
        return self.format_date(self.citv)

    def format_date(self, date_str):
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            return date.strftime('%d-%m-%Y')
        except ValueError:
            return date_str
    
    class Meta:
        db_table = "Notification"
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"