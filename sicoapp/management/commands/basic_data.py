from django.core.management.base import BaseCommand
from sicoapp.models import LicenseCategory, Fuel, TypeVehicle

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):

        licensecategory1 = LicenseCategory.objects.create(name='A-IIA')
        licensecategory2 = LicenseCategory.objects.create(name='A-IIB')
        licensecategory3 = LicenseCategory.objects.create(name='A-IIIA')
        licensecategory4 = LicenseCategory.objects.create(name='A-IIIB')
        licensecategory5 = LicenseCategory.objects.create(name='A-IIIC')

        fuel1 = Fuel.objects.create(name='G. REGULAR')
        fuel2 = Fuel.objects.create(name='G. PREMIUM')
        fuel3 = Fuel.objects.create(name='DIESEL')

        typevehicle1 = TypeVehicle.objects.create(name='VEHICULO')
        typevehicle2 = TypeVehicle.objects.create(name='MAQUINARIA')

        self.stdout.write(self.style.SUCCESS('Database successfully populated!'))
