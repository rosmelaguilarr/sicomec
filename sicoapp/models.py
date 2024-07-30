from django.db import models
from django.contrib.auth.models import User
import os
from django.core.validators import MinValueValidator
import uuid
from django.core.validators import RegexValidator
from django.utils import timezone



# STATIC MODELS --------------------------------------------------------------------

class LicenseCategory(models.Model):
    name = models.CharField(max_length=6, null=False, blank=False)

    def __str__(self):
        return self.name
    
class Fuel(models.Model):
    name = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return self.name

class TypeVehicle(models.Model):
    name = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return self.name
    


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
    name = models.CharField(max_length=20, verbose_name='Nombre', null=False, blank=False)
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
        return self.name

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
    plate = models.CharField(max_length=6, verbose_name='Placa/Reg.', null=False, blank=False)
    type = models.ForeignKey(TypeVehicle, on_delete=models.PROTECT, verbose_name='Tipo')
    name = models.CharField(max_length=30, verbose_name='Vehículo', null=False, blank=False)
    brand = models.CharField(max_length=20, verbose_name='Marca', null=False, blank=False)
    chassis = models.CharField(max_length=17, verbose_name='Chasis', null=False, blank=False)
    model = models.CharField(max_length=20, verbose_name='Modelo', null=False, blank=False)
    production = models.DateField(verbose_name='Fabricación', auto_now=False)
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

class FuelTap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ruc = models.CharField(max_length=11, verbose_name='RUC', unique=True,  null=False, blank=False, validators=[ruc_validator])
    business_name = models.CharField(max_length=70, verbose_name='Razón Social', null=False, blank=False)
    address = models.CharField(max_length=50, verbose_name='Dirección', null=False, blank=False)
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
        super(FuelTap, self).save(*args, **kwargs)



# BALLOT MODEL --------------------------------------------------------------------

class Ballot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True, editable=False)
    driver_dni = models.CharField(max_length=8)
    driver_name = models.CharField(max_length=20, verbose_name='Nombre')
    driver_last_name = models.CharField(max_length=30, verbose_name='Apellidos')
    driver_license = models.CharField(max_length=9, verbose_name='N° Licencia')
    driver_category = models.CharField(max_length=6, verbose_name='Categoría')
    drive_to = models.CharField(max_length=70, verbose_name='Sírvase conducir', null=False, blank=False)
    vehicle_plate = models.CharField(max_length=6, verbose_name='Placa')
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